import streamlit as st
import time

# Paleta de colores y rutas de los logos
PRIMARY_COLOR = "#4b83c0"
SECONDARY_COLOR = "#878889"
BACKGROUND_COLOR = "#f4f5f7"

ICOMEX_LOGO_PATH = "logos/ICOMEX_Logos_sin_fondo.png"
PAISA_BOT_LOGO_PATH = "logos/paisabot_avatar_transparent.png"


# Estilo personalizado
def render_custom_styles():
    st.markdown(
        f"""
        <style>
            .stApp {{
                background-color: {BACKGROUND_COLOR};
            }}
            .title {{
                color: {PRIMARY_COLOR};
                font-size: 2rem;
                font-weight: bold;
                margin-bottom: 0.5rem;
            }}
            .intro-text {{
                font-size: 1.3rem;
                line-height: 1.6;
                margin-bottom: 2rem;
                text-align: justify;
            }}
        </style>
        """,
        unsafe_allow_html=True,
    )

def render_title():
    logo_col1, logo_col2 = st.columns([1, 5], gap="medium")
    with logo_col1:
        st.image(PAISA_BOT_LOGO_PATH, use_container_width=True)
    with logo_col2:
        st.image(ICOMEX_LOGO_PATH, use_container_width=True)
    st.markdown('<div class="title">Paisa-Bot, asistente virtual</div>', unsafe_allow_html=True)

def render_subheader(mode):
    container = st.empty()
    text = mode.capitalize()
    displayed_text = ""
    for char in text:
        displayed_text += char
        container.subheader(displayed_text)
        time.sleep(0.05)

def render_intro():
    st.markdown(
        """
        <div class="intro-text">
        Soy <b>Paisa-Bot</b>, el agente de inteligencia artificial de la Agencia I-COMEX. 
        ¿Sobre qué tema querés interactuar hoy? Elegí un modo para empezar.
        </div>
        """,
        unsafe_allow_html=True,
    )

def render_input():
    return st.chat_input("Escribe tu mensaje aquí...")

def render_dynamic_message(message, avatar=None):
    if message["role"] == "assistant":
        with st.chat_message(message["role"], avatar=avatar):
            container = st.empty()
            text = message["content"]
            displayed_text = ""
            for char in text:
                displayed_text += char
                container.markdown(displayed_text)
                time.sleep(0.005)

def render_chat_message(role, content, avatar=None):
    with st.chat_message(role, avatar=avatar):
        st.markdown(content)
