import streamlit as st
import frontend
from openai import OpenAI
from PIL import Image

# Configuración de la página
PAISA_BOT_LOGO_PATH = "logos/paisabot_avatar.jpeg"
USER_LOGO_PATH = "logos/user_avatar.png"
st.set_page_config(page_title="Paisa-Bot - Asistente de IA", layout="centered", page_icon=PAISA_BOT_LOGO_PATH)

# Inicializar estilos personalizados
frontend.render_custom_styles()

# Cachear las imágenes
@st.cache_data
def load_image(image_path):
    return Image.open(image_path)

paisabot_logo = load_image(PAISA_BOT_LOGO_PATH)
user_logo = load_image(USER_LOGO_PATH)

# Inicialización del estado
if "selected_mode" not in st.session_state:
    st.session_state.selected_mode = None
if "messages" not in st.session_state:
    st.session_state.messages = []
if "initial_message_shown" not in st.session_state:
    st.session_state.initial_message_shown = False
if "subtitle_shown" not in st.session_state:
    st.session_state.subtitle_shown = False
if "rendered_message_ids" not in st.session_state:
    st.session_state.rendered_message_ids = set()

# Archivos de instrucciones del sistema
INSTRUCTIONS_FILES = {
    "Payador con IA 🎤🧉": "instructions_payador.txt",
    "Trivia 🤔🎲": "instructions_trivia.txt",
    "Mito o Realidad 🌟": "instructions_mito.txt",
    "Interacción Normal 🤝💬": "instructions_normal.txt",
}

# Obtener clave API de secrets
openai_api_key = st.secrets["openai"]["api_key"]

# Función para cargar instrucciones
def load_instructions(mode):
    try:
        with open(INSTRUCTIONS_FILES[mode], "r", encoding="utf-8") as file:
            return file.read().strip()
    except FileNotFoundError:
        st.error(f"No se encontró el archivo de instrucciones para {mode}.")
        return None

# Renderizar el encabezado (siempre visible)
frontend.render_title()

# Renderizar subtítulo dinámico basado en el modo seleccionado
if st.session_state.selected_mode:
    if not st.session_state.subtitle_shown:
        frontend.render_subheader(st.session_state.selected_mode)
        st.session_state.subtitle_shown = True
    else:
        st.subheader(st.session_state.selected_mode.capitalize())

# Renderizar la introducción y botones si no se ha seleccionado un modo
if st.session_state.selected_mode is None:
    frontend.render_intro()

# Mostrar chat y mensajes si se seleccionó un modo
if st.session_state.selected_mode:
    if not st.session_state.initial_message_shown:
        instructions = load_instructions(st.session_state.selected_mode)
        if instructions:
            st.session_state.messages.append({"role": "system", "content": instructions})
        st.session_state.messages.append({"role": "assistant", "content": st.session_state.initial_message})
        st.session_state.initial_message_shown = True

    # Renderizar mensajes existentes
    for i, message in enumerate(st.session_state.messages):
        if message["role"] != "system":
            message_id = f"{message['role']}-{i}"
            if message_id not in st.session_state.rendered_message_ids:
                if message["role"] == "assistant":
                    frontend.render_dynamic_message(message, avatar=paisabot_logo)
                else:
                    frontend.render_chat_message(message["role"], message["content"], avatar=user_logo)
                st.session_state.rendered_message_ids.add(message_id)

    # Renderizar el campo de entrada
    if prompt := frontend.render_input():
        st.session_state.messages.append({"role": "user", "content": prompt})
        frontend.render_chat_message("user", prompt, avatar=user_logo)

        client = OpenAI(api_key=openai_api_key)

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=st.session_state.messages,
            temperature=0.2
        )

        response_content = response.choices[0].message.content
        response_message = {"role": "assistant", "content": response_content}
        st.session_state.messages.append(response_message)

        frontend.render_dynamic_message(response_message, avatar=paisabot_logo)
        st.session_state.rendered_message_ids.add(f"assistant-{len(st.session_state.messages) - 1}")
