import streamlit as st
import frontend
from openai import OpenAI
from PIL import Image
import tempfile
import emoji
import re
from elevenlabs import ElevenLabs
from pydub import AudioSegment
import random

# Configuración de la página
PRIMARY_COLOR = "#4b83c0"
SECONDARY_COLOR = "#878889"
BACKGROUND_COLOR = "#ffffff"

ICOMEX_LOGO_PATH = "logos/ICOMEX_Logos_sin_fondo.png"
PAISA_AVATAR_PATH = "logos/paisabot_avatar_chat.png"
USER_LOGO_PATH = "logos/user_avatar.png"

st.set_page_config(page_title="PaisaBot - Asesor Virtual", layout="centered", page_icon=PAISA_AVATAR_PATH)

# Inicializar estilos personalizados
frontend.render_custom_styles()

background_tracks = [
    {"path": "instrumentales/milonga_arrabalera_1.mp3", "total_duration": 103, "intro_duration": 14},
    {"path": "instrumentales/milonga_arrabalera_2.mp3", "total_duration": 25, "intro_duration": 10},
    {"path": "instrumentales/milonga_arrabalera_3.mp3", "total_duration": 29, "intro_duration": 11},
    {"path": "instrumentales/milonga_arrabalera_4.mp3", "total_duration": 56, "intro_duration": 10.5},
    {"path": "instrumentales/milonga_arrabalera_5.mp3", "total_duration": 31, "intro_duration": 6},
    {"path": "instrumentales/milonga_campera_1.mp3", "total_duration": 118, "intro_duration": 9},
    {"path": "instrumentales/milonga_campera_2.mp3", "total_duration": 80, "intro_duration": 1},
    {"path": "instrumentales/milonga_campera_3.mp3", "total_duration": 38, "intro_duration": 1},
    {"path": "instrumentales/milonga_campera_4.mp3", "total_duration": 110, "intro_duration": 16},
    {"path": "instrumentales/milonga_campera_5.mp3", "total_duration": 190, "intro_duration": 16},
    {"path": "instrumentales/milonga_oriental_1.mp3", "total_duration": 126, "intro_duration": 12},
    {"path": "instrumentales/milonga_oriental_2.mp3", "total_duration": 116, "intro_duration": 1},
    {"path": "instrumentales/milonga_oriental_3.mp3", "total_duration": 71, "intro_duration": 1},
    {"path": "instrumentales/milonga_oriental_4.mp3", "total_duration": 41, "intro_duration": 12},
    {"path": "instrumentales/milonga_oriental_5.mp3", "total_duration": 30, "intro_duration": 1},
    {"path": "instrumentales/milonga_pampeana_1.mp3", "total_duration": 101, "intro_duration": 17},
    {"path": "instrumentales/milonga_pampeana_2.mp3", "total_duration": 101, "intro_duration": 1},
    {"path": "instrumentales/milonga_pampeana_3.mp3", "total_duration": 84, "intro_duration": 1},
    {"path": "instrumentales/milonga_pampeana_4.mp3", "total_duration": 69, "intro_duration": 14.5},
    {"path": "instrumentales/milonga_pampeana_5.mp3", "total_duration": 69, "intro_duration": 0.5},
    {"path": "instrumentales/milonga_pampeana_6.mp3", "total_duration": 55, "intro_duration": 1},
    {"path": "instrumentales/milonga_pampeana_7.mp3", "total_duration": 25, "intro_duration": 1},
    {"path": "instrumentales/milonga_payada_1.mp3", "total_duration": 125, "intro_duration": 1},
    {"path": "instrumentales/milonga_payada_2.mp3", "total_duration": 53, "intro_duration": 1},
]

def combine_audio_with_background(voice_path):
    """
    Combina el audio generado con una pista de fondo en formato MP3.
    Incrementa el volumen de la voz un 35%.
    """
    try:
        # Cargar el audio de la voz
        voice_audio = AudioSegment.from_file(voice_path)

        # Aumentar el volumen de la voz en un 35%
        voice_audio = voice_audio + 35 / 10  # Convertir porcentaje a dB (decibelios)

        voice_duration = len(voice_audio) / 1000  # Duración en segundos

        # Filtrar pistas válidas
        valid_tracks = [
            track for track in background_tracks
            if track["total_duration"] >= voice_duration + track["intro_duration"] + 2
        ]

        if not valid_tracks:
            st.error("No hay pistas musicales disponibles que cumplan con los requisitos.")
            return None

        # Seleccionar una pista al azar
        selected_track = random.choice(valid_tracks)
        background_audio = AudioSegment.from_file(selected_track["path"])

        # Recortar la pista de fondo
        total_cut_duration = selected_track["intro_duration"] + voice_duration + 2
        trimmed_background = background_audio[:total_cut_duration * 1000]

        # Superponer la voz
        combined_audio = trimmed_background.overlay(voice_audio, position=selected_track["intro_duration"] * 1000)

        # Aplicar fade out en los últimos 2 segundos
        final_audio = combined_audio.fade_out(duration=2000)

        # Exportar el audio combinado
        output_path = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3").name
        final_audio.export(output_path, format="mp3")

        return output_path

    except Exception as e:
        st.error(f"Error al combinar audio: {e}")
        return None

# Cachear las imágenes
@st.cache_data
def load_image(image_path):
    return Image.open(image_path)

def clean_message_for_audio(message_content):
    # Replace for pronunciation
    message_content = message_content.replace("I-COMEX","ICÓMEX")
    message_content = message_content.replace("km","kilómetros")
    message_content = message_content.replace("1950", "mil novecientos cincuenta")
    message_content = message_content.replace("2954575326", "dos nueve cinco cuatro, cincuenta y siete, cincuenta y tres, veintiseis.")
    message_content = message_content.replace("agencia@icomexlapampa.org","agencia, arroba, icomexlapampa, punto, org.")
    message_content = message_content.replace("08:00 a 15:00 hs","ocho a quince horas")
    message_content = message_content.replace("https://maps.app.goo.gl/RET62U9mK9JecpmT9","")
    message_content = message_content.replace("!",".")
    message_content = message_content.replace("¡","")
    # Remove Markdown bold (**text** -> text)
    message_content = re.sub(r"\*\*(.*?)\*\*", r"\1", message_content)
    # Remove emojis
    message_content = emoji.replace_emoji(message_content, replace="")
    # Remove all "#" characters
    message_content = message_content.replace("#", "")
    # Replace line breaks with spaces
    message_content = message_content.replace(":", "...")
    
    # Reemplazar párrafos que terminan en punto seguido de salto de línea doble por "..."
    #message_content = re.sub(r'\,\s*\n', '--\n', message_content)
    #message_content = re.sub(r'\.\s*\n\s*\n', ' <break time="3s" />\n\n', message_content)
    message_content = message_content.replace(".", '<break time="1s" />')
    message_content = re.sub(r'<break time="1s" />  $', '.', message_content)
    message_content = re.sub(r'<break time="1s" />$', '.', message_content)    
    return message_content

# Function to load instructions
def load_instructions(topic):
    INSTRUCTIONS_FILES = {
        "Mito o realidad": "instructions\instructions_mito_realidad.txt",
        "Trivia": "instructions\instructions_trivia.txt",
        "Payador con IA": "instructions\instructions_payador.txt"
    }
    try:
        with open(INSTRUCTIONS_FILES[topic], "r", encoding="utf-8") as file:
            return file.read().strip()
    except FileNotFoundError:
        st.error(f"No se encontró el archivo de instrucciones para {topic}.")
        return None

paisa_logo = load_image(PAISA_AVATAR_PATH)
user_logo = load_image(USER_LOGO_PATH)

# Inicialización del estado
if "selected_topic" not in st.session_state:
    st.session_state.selected_topic = None
if "messages" not in st.session_state:
    st.session_state.messages = []
if "initial_message_shown" not in st.session_state:
    st.session_state.initial_message_shown = False
if "subtitle_shown" not in st.session_state:
    st.session_state.subtitle_shown = False
if "rendered_message_ids" not in st.session_state:
    st.session_state.rendered_message_ids = set()
if "show_form" not in st.session_state:
    st.session_state.show_form = False

# Renderizar el encabezado (siempre visible)
frontend.render_title()

def generar_audio_elevenlabs_sdk(texto, voice_id="ZtseFBfK9giRDiPkiE6o"):
    try:
        # Inicializa el cliente de ElevenLabs con la clave API
        client = ElevenLabs(api_key=st.secrets["elevenlabs"]["api_key"])

        # Generar el audio usando el SDK
        audio_generator = client.text_to_speech.convert(
            voice_id=voice_id,
            model_id="eleven_multilingual_v2",
            text=texto,
            voice_settings={
                "stability": 0.30,
                "similarity_boost": 0.77,
                "style": 0.8,
                "use_speaker_boost": True
            }
        )

        # Guardar en un archivo temporal
        temp_audio = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
        with open(temp_audio.name, "wb") as f:
            for chunk in audio_generator:  # Iterar sobre el generador
                f.write(chunk)

        return temp_audio.name

    except Exception as e:
        st.error(f"Error al generar audio: {e}")
        return None

# Renderizar subtítulo dinámico basado en el tema seleccionado
if st.session_state.selected_topic:
    if not st.session_state.subtitle_shown:
        frontend.render_subheader(st.session_state.selected_topic)
        st.session_state.subtitle_shown = True
    else:
        st.subheader(st.session_state.selected_topic)

# Renderizar la introducción y botones solo si no se ha seleccionado un tema
if st.session_state.selected_topic is None:
    frontend.render_intro()

# Mostrar chat y mensajes si se seleccionó un tema
if st.session_state.selected_topic:
    # Cargar las instrucciones del sistema solo una vez
    if not st.session_state.initial_message_shown:
        instructions = load_instructions(st.session_state.selected_topic)
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
                    frontend.render_dynamic_message(message, avatar=paisa_logo)
                else:
                    frontend.render_chat_message(message["role"], message["content"], avatar=user_logo)
                st.session_state.rendered_message_ids.add(message_id)
            else:
                frontend.render_chat_message(message["role"], message["content"],
                                             avatar=paisa_logo if message["role"] == "assistant" else user_logo)

    # Renderizar el campo de entrada
    if prompt := frontend.render_input():
        st.session_state.messages.append({"role": "user", "content": prompt})
        frontend.render_chat_message("user", prompt, avatar=user_logo)

        client = OpenAI(api_key=st.secrets["openai"]["api_key"])
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=st.session_state.messages,
            temperature=1,                    
            frequency_penalty=0, 
            presence_penalty=-1   
        )

        response_content = response.choices[0].message.content
        response_message = {"role": "assistant", "content": response_content}
        st.session_state.messages.append(response_message)

        # Renderizar el mensaje del chatbot
        frontend.render_dynamic_message(response_message, avatar=paisa_logo)
        st.session_state.rendered_message_ids.add(f"assistant-{len(st.session_state.messages) - 1}")

        # Limpiar el texto antes de enviarlo a Eleven Labs
        texto_limpio = clean_message_for_audio(response_content)
        # Generar el audio de la voz
        audio_path = generar_audio_elevenlabs_sdk(texto_limpio)
        if audio_path:
            # Combinar con música de fondo
            final_audio_path = combine_audio_with_background(audio_path)
            if final_audio_path:
                st.audio(final_audio_path, format="audio/mp3")