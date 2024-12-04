import streamlit as st
import time

# Paleta de colores y rutas de los logos
PRIMARY_COLOR = "#4b83c0"
SECONDARY_COLOR = "#878889"
BACKGROUND_COLOR = "#f4f5f7"

ICOMEX_LOGO_PATH = "logos/ICOMEX_Logos_sin_fondo.png"
PAISA_LOGO_PATH = "logos/paisabot_avatar_transparent.png"

# Estilo personalizado
def render_custom_styles():
    st.markdown(
        f"""
        <style>
            .stApp {{
                background-color: {BACKGROUND_COLOR};
            }}
            input {{
                border: 1px solid {SECONDARY_COLOR}; /* Input border color */
                border-radius: 5px; /* Rounded corners */
                padding: 8px;
            }}
            textarea {{
                border: 1px solid {SECONDARY_COLOR}; /* Textarea border color */
                border-radius: 5px; /* Rounded corners */
                padding: 8px;
            }}
            .title {{
                color: {PRIMARY_COLOR};
                font-size: 2.5rem;
                font-weight: bold;
                margin-bottom: 0rem;
            }}
            .intro-text {{
                font-size: 1.35rem;
                line-height: 1.6;  /* Ajustar espaciado entre líneas */
                margin-bottom: 0rem;
                text-align: justify; /* Justificar texto */
            }}
            .intro-question {{
                font-size: 1.5rem;
                font-weight: bold;
                text-align: center;
                margin-bottom: 1rem;
            }}
            .stButton>button {{
                background-color: {SECONDARY_COLOR};
                color: white;
                border: none;
                border-radius: 10px;
                padding: 12px 24px;
                font-size: 30px !important;
                transition: background-color 0.3s ease;
            }}
            .stButton>button:hover {{
                background-color: {PRIMARY_COLOR};
                color: white;
            }}
            .button-container {{
                display: flex;
                justify-content: center;
                gap: 1.5rem;
                margin-top: 2rem;
            }}
        </style>
        """,
        unsafe_allow_html=True,
    )


# Render the title with centered logos
def render_title():
    # Create columns with relative proportions
    logo_col1, logo_col2 = st.columns([1, 4], gap="medium", vertical_alignment="center")

    # Add images to the columns and center them
    with logo_col1:
        # Center the image in the column
        with st.container():
            st.image(PAISA_LOGO_PATH, use_container_width=True)
    with logo_col2:
        # Center the image in the column
        with st.container():
            st.image(ICOMEX_LOGO_PATH, use_container_width=True)

    # Add a title below the logos, centered
    st.markdown(
        '<div class="title";">PaisaBot, asesor virtual</div>',
        unsafe_allow_html=True,
    )

# Renderizar subtítulo con efecto de escritura
def render_subheader(topic):
    container = st.empty()  # Crear un contenedor vacío para el texto dinámico
    text = topic
    displayed_text = ""
    for char in text:
        displayed_text += char
        container.subheader(displayed_text)  # Actualizar el contenedor
        time.sleep(0.0)

# Renderizar mensajes con efecto de escritura
def render_messages(messages):
    for message in messages:
        if message["role"] != "system":
            with st.chat_message(message["role"]):
                container = st.empty()
                text = message["content"]
                displayed_text = ""
                for char in text:
                    displayed_text += char
                    container.markdown(displayed_text)
                    time.sleep(0.002)

# Renderizar campo de entrada
def render_input():
    return st.chat_input("Escribe tu mensaje aquí...")

# Renderizar la introducción y los botones iniciales
def render_intro():
    st.markdown(
        """
        <div class="intro-text">
        Soy <b>PaisaBot</b>, el asesor virtual de IA de la Agencia I-COMEX. Conozcamos más sobre comercio exterior e inversiones en La Pampa jugando.<br><br>
        </div>
        <div class="intro-question">
        Elegí un modo de interacción
        </div>
        """,
        unsafe_allow_html=True,
    )


    # Uso directo de columnas para los botones
    btn_col1, btn_col2, btn_col3 = st.columns(3, gap="medium")
    with btn_col1:
        st.button(
            "**Mito o Realidad 🤔❓**",
            key="intro_mito_realidad",
            on_click=select_mito_realidad,  # Conecta el callback
            use_container_width=True,
        )
    with btn_col2:
        st.button(
            "**Trivia 🎲🎯**",
            key="intro_trivia",
            on_click=select_trivia,  # Conecta el callback
            use_container_width=True,
        )
    with btn_col3:
        st.button(
            "**Payador con IA 🎤🧉**",
            key="intro_payador",
            on_click=select_payador,  # Conecta el callback
            use_container_width=True,
        )

# Funciones de selección
def select_mito_realidad():
    st.session_state.selected_topic = "Mito o realidad"
    st.session_state.initial_message = (
        "¡Hola! Soy PaisaBot 😊. "
        "Te voy a mostrar una afirmación o pregunta relacionada a la economía pampeana y me dirás si es **Mito** o **Realidad**. "
        "Pensá con cuidado porque haremos solo 5 rondas. "
        "Decime cómo te llamás y comencemos, ¿dale?"
    )
    st.session_state.initial_message_shown = False

def select_trivia():
    st.session_state.selected_topic = "Trivia"
    st.session_state.initial_message = (
    "¡Hola! Soy PaisaBot 😊. "
    "Juguemos a la trivia, es fácil: te haré una **pregunta con opciones y deberás adivinar la correcta**. Tendrás 5 oportunidades, así que piensa bien. Decime tu nombre para comenzar, ¿te parece?"
    )
    st.session_state.initial_message_shown = False

def select_payador():
    st.session_state.selected_topic = "Payador con IA"
    st.session_state.initial_message = (
    "¡Soy PaisaBot, te saludo!  \n"
    "Así que buscás payada,  \n"
    "estás en charla adecuada,  \n"
    "con mi canto yo acudo.  \n"
    "De **inversiones** soy escudo,  \n"
    "**comercio exterior** mi camino,  \n"
    "como buen pampeano y argentino.  \n"
    "Contame qué te interesa,  \n"
    "mi payada te lo expresa,  \n"
    "¡elegí bien te pido!  \n"
    "\n"
    "**Temáticas sugeridas: productos y destinos de exportación, oportunidades de inversión, rondas de negocios, ferias internacionales,  Centro de Negocios de Neuquén, Agencia I-COMEX?**"
)

    st.session_state.initial_message_shown = False

def render_dynamic_message(message, avatar=None):
    if message["role"] == "assistant":
        with st.chat_message(message["role"], avatar=avatar):
            container = st.empty()
            text = message["content"]
            displayed_text = ""
            for char in text:
                displayed_text += char
                container.markdown(displayed_text)
                time.sleep(0.0005)

# Renderizar mensaje estático con avatar
def render_chat_message(role, content, avatar=None):
    with st.chat_message(role, avatar=avatar):
        st.markdown(content)
