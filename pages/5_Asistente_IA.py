
import streamlit as st
import unicodedata

from utils.state import initialize_state, load_diseases
from utils.theme import apply_theme, page_header


# =========================================================
# CONFIGURACIÓN INICIAL
# =========================================================

st.set_page_config(
    page_title="Asistente de investigación | Operación Oropouche",
    page_icon="💬",
    layout="wide"
)

initialize_state()
apply_theme("asistente")


# =========================================================
# ESTILOS DEL MÓDULO
# =========================================================

st.markdown(
    """
    <style>
    .assistant-intro {
        color: #5F6070;
        font-size: 1rem;
        line-height: 1.65;
        max-width: 850px;
        margin-bottom: 1.2rem;
    }

    .assistant-label {
        color: #5D5579;
        font-size: 0.76rem;
        font-weight: 700;
        letter-spacing: 0.10em;
        text-transform: uppercase;
        margin-bottom: 0.35rem;
    }

    .assistant-muted {
        color: #696879;
        font-size: 0.88rem;
        line-height: 1.55;
    }

    .assistant-notice {
        background: rgba(255, 255, 255, 0.65);
        border: 1px solid rgba(100, 90, 125, 0.17);
        border-radius: 12px;
        padding: 1rem 1.1rem;
    }

    [data-testid="stChatMessage"] {
        border: 1px solid rgba(100, 90, 125, 0.12);
        border-radius: 12px;
        padding: 1rem;
    }
    </style>
    """,
    unsafe_allow_html=True
)


# =========================================================
# ENCABEZADO
# =========================================================

page_header(
    "Asistente de investigación",
    "Consulta la biblioteca científica y explora información "
    "sobre las enfermedades contempladas en la simulación.",
    "MÓDULO 05 · CONSULTA Y ORIENTACIÓN"
)

st.markdown(
    """
    <p class="assistant-intro">
        Consulta información sobre manifestaciones clínicas,
        agentes etiológicos, vectores, pruebas diagnósticas
        y características epidemiológicas. Utiliza esta
        información para complementar la investigación de
        los expedientes y construir hipótesis diferenciales.
    </p>
    """,
    unsafe_allow_html=True
)


# =========================================================
# CARGA DE INFORMACIÓN
# =========================================================

diseases = load_diseases()

if not isinstance(diseases, dict) or not diseases:

    st.warning(
        "No se encontró información en la biblioteca de enfermedades. "
        "Verifica el archivo data/enfermedades.json."
    )

    st.stop()


# =========================================================
# FUNCIONES AUXILIARES
# =========================================================

def normalize_text(value):
    """
    Normaliza texto para facilitar la búsqueda
    sin diferenciar mayúsculas ni tildes.
    """

    if value is None:
        return ""

    value = str(value).casefold()
    value = unicodedata.normalize("NFD", value)

    return "".join(
        character
        for character in value
        if unicodedata.category(character) != "Mn"
    )


def format_value(value):
    """
    Convierte listas, diccionarios y otros valores
    en texto legible.
    """

    if value is None:
        return "No hay información registrada."

    if isinstance(value, list):

        if not value:
            return "No hay información registrada."

        return "\n".join(
            f"- {format_value(item)}"
            for item in value
        )

    if isinstance(value, dict):

        if not value:
            return "No hay información registrada."

        return "\n".join(
            f"- **{str(key).replace('_', ' ').capitalize()}:** "
            f"{format_value(item)}"
            for key, item in value.items()
        )

    return str(value)


# =========================================================
# ALIAS DE ENFERMEDADES
# =========================================================

DISEASE_ALIASES = {
    "oropouche": [
        "oropouche",
        "oropuche"
    ],
    "dengue": [
        "dengue"
    ],
    "chikungunya": [
        "chikungunya",
        "chikunguna"
    ],
    "zika": [
        "zika"
    ],
    "fiebre_amarilla": [
        "fiebre amarilla",
        "fiebre_amarilla"
    ],
    "mayaro": [
        "mayaro"
    ],
    "malaria": [
        "malaria",
        "paludismo"
    ],
    "leptospirosis": [
        "leptospirosis",
        "leptospira"
    ]
}


def find_mentioned_diseases(question, disease_data):
    """
    Identifica todas las enfermedades mencionadas
    en una consulta.
    """

    normalized_question = normalize_text(question)

    found = []

    for disease_id, item in disease_data.items():

        if not isinstance(item, dict):
            continue

        aliases = [
            disease_id.replace("_", " "),
            item.get("nombre", disease_id)
        ]

        aliases.extend(
            DISEASE_ALIASES.get(disease_id, [])
        )

        for alias in aliases:

            normalized_alias = normalize_text(alias)

            if (
                normalized_alias
                and normalized_alias in normalized_question
            ):

                if disease_id not in found:
                    found.append(disease_id)

                break

    return found


def find_disease(question, disease_data):
    """
    Identifica la primera enfermedad mencionada.
    """

    found = find_mentioned_diseases(
        question,
        disease_data
    )

    return found[0] if found else None


# =========================================================
# IDENTIFICACIÓN DEL TEMA CONSULTADO
# =========================================================

TOPIC_KEYWORDS = {
    "manifestaciones": [
        "sintoma",
        "sintomas",
        "manifestacion",
        "manifestaciones",
        "signos clinicos",
        "cuadro clinico",
        "presenta",
        "clinica"
    ],
    "pruebas": [
        "prueba",
        "pruebas",
        "laboratorio",
        "pcr",
        "ns1",
        "serologia",
        "diagnostico de laboratorio",
        "deteccion"
    ],
    "vector": [
        "vector",
        "mosquito",
        "insecto",
        "transmite",
        "transmision"
    ],
    "agente": [
        "agente",
        "virus",
        "bacteria",
        "parasito",
        "etiologico",
        "causa"
    ],
    "pistas": [
        "epidemiologia",
        "epidemiologico",
        "exposicion",
        "zona",
        "riesgo",
        "ambiente",
        "reservorio"
    ],
    "consideraciones": [
        "consideracion",
        "consideraciones",
        "precaucion",
        "embarazo",
        "complicacion",
        "importante"
    ]
}


TOPIC_LABELS = {
    "manifestaciones": "Manifestaciones clínicas",
    "pruebas": "Pruebas diagnósticas",
    "vector": "Vector",
    "agente": "Agente etiológico",
    "pistas": "Pistas epidemiológicas",
    "consideraciones": "Consideraciones"
}


def detect_topic(question):
    """
    Identifica el tema principal de una consulta.
    """

    normalized_question = normalize_text(question)

    for topic, keywords in TOPIC_KEYWORDS.items():

        if any(
            normalize_text(keyword) in normalized_question
            for keyword in keywords
        ):
            return topic

    return None


# =========================================================
# RESPUESTAS SOBRE ENFERMEDADES
# =========================================================

def disease_response(disease_id, item):
    """
    Construye una respuesta completa sobre una enfermedad.
    """

    name = item.get("nombre", disease_id.capitalize())

    response = [
        f"### {name}",
        "",
        format_value(item.get("descripcion")),
        ""
    ]

    fields = [
        ("agente", "Agente etiológico"),
        ("vector", "Vector"),
        ("manifestaciones", "Manifestaciones clínicas"),
        ("pistas", "Pistas epidemiológicas"),
        ("pruebas", "Pruebas diagnósticas"),
        ("consideraciones", "Consideraciones")
    ]

    for field, label in fields:

        value = item.get(field)

        if value:

            response.extend([
                f"**{label}:**",
                format_value(value),
                ""
            ])

    if disease_id == "zika":

        response.extend([
            "**Aspecto adicional:**",
            "Es importante investigar la posibilidad de "
            "embarazo debido a los riesgos asociados a la "
            "infección durante la gestación.",
            ""
        ])

    elif disease_id == "dengue":

        response.extend([
            "**Aspecto adicional:**",
            "Se deben reconocer oportunamente los signos "
            "de alarma y considerar la evolución clínica.",
            ""
        ])

    elif disease_id == "oropouche":

        response.extend([
            "**Aspecto adicional:**",
            "Sus manifestaciones pueden superponerse con "
            "las de otras arbovirosis. Por ello, el contexto "
            "epidemiológico y las pruebas diagnósticas "
            "son relevantes.",
            ""
        ])

    response.extend([
        "---",
        "Esta información sirve como referencia académica. "
        "La interpretación debe considerar el contexto clínico "
        "y epidemiológico completo."
    ])

    return "\n".join(response)


def topic_response(disease_id, item, topic):
    """
    Responde específicamente sobre un aspecto
    de una enfermedad.
    """

    name = item.get("nombre", disease_id.capitalize())

    if topic not in item or not item.get(topic):

        return (
            f"### {TOPIC_LABELS.get(topic, 'Información')}\n\n"
            f"La biblioteca del proyecto no contiene información "
            f"específica sobre este aspecto de {name}."
        )

    return (
        f"### {TOPIC_LABELS.get(topic, 'Información')} · {name}\n\n"
        f"{format_value(item.get(topic))}\n\n"
        "---\n"
        "La información es de carácter académico y debe "
        "interpretarse junto con el contexto del paciente."
    )


# =========================================================
# COMPARACIÓN DE ENFERMEDADES
# =========================================================

def compare_diseases(disease_ids, disease_data):
    """
    Compara los campos disponibles de dos o más enfermedades.
    """

    if len(disease_ids) < 2:

        return (
            "### Orientación para el diagnóstico diferencial\n\n"
            "Menciona al menos dos enfermedades para consultar "
            "sus diferencias específicas.\n\n"
            "En la comparación se deben considerar las "
            "manifestaciones clínicas, los vectores, los "
            "antecedentes epidemiológicos y las pruebas."
        )

    fields = [
        ("agente", "Agente etiológico"),
        ("vector", "Vector"),
        ("manifestaciones", "Manifestaciones clínicas"),
        ("pistas", "Pistas epidemiológicas"),
        ("pruebas", "Pruebas diagnósticas")
    ]

    response = [
        "### Comparación de enfermedades",
        ""
    ]

    for disease_id in disease_ids:

        item = disease_data.get(disease_id, {})

        if not isinstance(item, dict):
            continue

        response.extend([
            f"#### {item.get('nombre', disease_id)}",
            ""
        ])

        for field, label in fields:

            value = item.get(field)

            if value:

                response.extend([
                    f"**{label}:**",
                    format_value(value),
                    ""
                ])

        response.append("---")

    response.extend([
        "",
        "**Criterios para el análisis diferencial**",
        "",
        "- Contexto geográfico y epidemiológico.",
        "- Antecedentes de exposición a vectores.",
        "- Tiempo de evolución de los síntomas.",
        "- Manifestaciones clínicas predominantes.",
        "- Resultados de las pruebas diagnósticas.",
        "- Signos de alarma y evolución del paciente.",
        "",
        "La presencia de fiebre, cefalea o mialgia no "
        "permite distinguir por sí sola entre todas "
        "estas enfermedades."
    ])

    return "\n".join(response)


# =========================================================
# GENERACIÓN DE RESPUESTAS
# =========================================================

def generate_response(question, disease_data):
    """
    Genera respuestas mediante reglas y consulta
    de la biblioteca local de enfermedades.
    """

    text = normalize_text(question)

    # -----------------------------------------------------
    # 1. Signos de alarma
    # -----------------------------------------------------

    if any(
        word in text
        for word in [
            "signos de alarma",
            "alarma",
            "urgencia",
            "urgente"
        ]
    ):

        return (
            "### Reconocimiento de signos de alarma\n\n"
            "En el dengue, algunos hallazgos que requieren "
            "valoración prioritaria incluyen:\n\n"
            "- Dolor abdominal intenso o continuo.\n"
            "- Vómitos persistentes.\n"
            "- Sangrado de mucosas.\n"
            "- Acumulación de líquidos.\n"
            "- Letargo, irritabilidad o deterioro clínico.\n"
            "- Signos de compromiso circulatorio.\n\n"
            "La identificación de estos hallazgos debe orientar "
            "una valoración clínica oportuna. No se debe retrasar "
            "la atención para completar pruebas o actividades "
            "de esta simulación."
        )

    # -----------------------------------------------------
    # 2. Identificación de enfermedades
    # -----------------------------------------------------

    mentioned_diseases = find_mentioned_diseases(
        question,
        disease_data
    )

    # -----------------------------------------------------
    # 3. Comparación específica
    # -----------------------------------------------------

    is_comparison = any(
        word in text
        for word in [
            "diferencial",
            "comparar",
            "comparacion",
            "diferencia",
            "diferencias",
            "se parecen",
            "parecido"
        ]
    )

    if is_comparison:

        return compare_diseases(
            mentioned_diseases,
            disease_data
        )

    # -----------------------------------------------------
    # 4. Consulta específica de una enfermedad
    # -----------------------------------------------------

    disease_id = find_disease(
        question,
        disease_data
    )

    if disease_id:

        item = disease_data.get(disease_id, {})

        if not isinstance(item, dict):
            item = {}

        topic = detect_topic(question)

        if topic:

            return topic_response(
                disease_id,
                item,
                topic
            )

        return disease_response(
            disease_id,
            item
        )

    # -----------------------------------------------------
    # 5. Consulta general sobre pruebas
    # -----------------------------------------------------

    if any(
        word in text
        for word in [
            "prueba",
            "laboratorio",
            "pcr",
            "ns1",
            "serologia"
        ]
    ):

        return (
            "### Selección de pruebas diagnósticas\n\n"
            "La elección de una prueba depende de varios elementos:\n\n"
            "- Enfermedad que se sospecha.\n"
            "- Día de evolución de los síntomas.\n"
            "- Tipo y calidad de la muestra.\n"
            "- Disponibilidad y características de la prueba.\n"
            "- Contexto clínico y epidemiológico.\n\n"
            "En términos generales, las pruebas moleculares "
            "pueden identificar material genético del agente "
            "durante ventanas específicas de la infección, "
            "mientras que las pruebas serológicas detectan "
            "la respuesta inmunológica.\n\n"
            "Consulta el módulo **Laboratorio diagnóstico** "
            "para explorar las pruebas configuradas en el proyecto."
        )

    # -----------------------------------------------------
    # 6. Consulta general sobre diagnóstico diferencial
    # -----------------------------------------------------

    if any(
        word in text
        for word in [
            "diagnostico",
            "enfermedades",
            "arbovirosis",
            "fiebre",
            "diferencial"
        ]
    ):

        names = [
            item.get("nombre", disease_id)
            for disease_id, item in disease_data.items()
            if isinstance(item, dict)
        ]

        return (
            "### Orientación para la investigación\n\n"
            "Para estudiar un cuadro febril y construir "
            "un diagnóstico diferencial, considera:\n\n"
            "1. Contexto geográfico y epidemiológico.\n"
            "2. Antecedentes de exposición a vectores.\n"
            "3. Tiempo de evolución de los síntomas.\n"
            "4. Manifestaciones clínicas predominantes.\n"
            "5. Resultados de las pruebas diagnósticas.\n"
            "6. Signos de alarma y evolución del paciente.\n\n"
            f"**Enfermedades disponibles:** {', '.join(names)}.\n\n"
            "La presencia de fiebre, cefalea o mialgia "
            "no permite establecer por sí sola una enfermedad."
        )

    # -----------------------------------------------------
    # 7. Respuesta general
    # -----------------------------------------------------

    available_names = ", ".join(
        item.get("nombre", disease_id)
        for disease_id, item in disease_data.items()
        if isinstance(item, dict)
    )

    return (
        "### Consulta de investigación\n\n"
        "Puedo ayudarte a explorar la información disponible "
        "en la biblioteca científica del proyecto.\n\n"
        f"**Enfermedades incluidas:** {available_names}.\n\n"
        "**Puedes consultar, por ejemplo:**\n\n"
        "- ¿Cuáles son las manifestaciones del Oropouche?\n"
        "- ¿Qué pruebas se utilizan para investigar dengue?\n"
        "- ¿Cuál es el vector del virus Mayaro?\n"
        "- ¿Qué diferencias existen entre dengue y chikungunya?\n"
        "- ¿Qué signos de alarma deben reconocerse?\n\n"
        "Intenta mencionar una enfermedad, una prueba "
        "o un aspecto clínico concreto."
    )


# =========================================================
# INICIALIZACIÓN DE LA CONVERSACIÓN
# =========================================================

welcome_message = {
    "role": "assistant",
    "content": (
        "Bienvenido al asistente de investigación.\n\n"
        "Puedes consultar información sobre las enfermedades "
        "incluidas en la biblioteca, sus manifestaciones clínicas, "
        "vectores, agentes etiológicos y pruebas diagnósticas.\n\n"
        "También puedes comparar enfermedades para explorar "
        "sus diferencias clínicas y epidemiológicas.\n\n"
        "¿Qué deseas investigar?"
    )
}

if (
    "assistant_messages" not in st.session_state
    or not isinstance(st.session_state.assistant_messages, list)
):
    st.session_state.assistant_messages = [
        welcome_message
    ]


# =========================================================
# PANEL INFORMATIVO
# =========================================================

with st.container(border=True):

    st.markdown(
        '<div class="assistant-label">ALCANCE DEL ASISTENTE</div>',
        unsafe_allow_html=True
    )

    st.write(
        "El asistente consulta información local almacenada "
        "en `data/enfermedades.json` y utiliza reglas de búsqueda "
        "por palabras clave para organizar las respuestas."
    )

    st.caption(
        "Esta versión funciona mediante reglas locales. "
        "No utiliza un modelo generativo conectado ni realiza "
        "diagnósticos médicos autónomos."
    )


# =========================================================
# HISTORIAL DEL CHAT
# =========================================================

st.divider()

st.markdown("### Conversación de investigación")

for message in st.session_state.assistant_messages:

    if not isinstance(message, dict):
        continue

    role = message.get("role")
    content = message.get("content", "")

    if role not in ("assistant", "user"):
        continue

    with st.chat_message(role):
        st.markdown(content)


# =========================================================
# ENTRADA DEL USUARIO
# =========================================================

question = st.chat_input(
    "Escribe tu consulta de investigación...",
    key="assistant_chat_input"
)

if question:

    st.session_state.assistant_messages.append({
        "role": "user",
        "content": question
    })

    answer = generate_response(
        question,
        diseases
    )

    st.session_state.assistant_messages.append({
        "role": "assistant",
        "content": answer
    })

    st.rerun()


# =========================================================
# CONTROLES DE CONVERSACIÓN
# =========================================================

st.divider()

col_info, col_clear = st.columns([3, 1])

with col_info:

    st.caption(
        f"Mensajes en la conversación: "
        f"{len(st.session_state.assistant_messages)}"
    )

with col_clear:

    if st.button(
        "Limpiar conversación",
        use_container_width=True
    ):

        st.session_state.assistant_messages = [
            welcome_message
        ]

        st.rerun()


# =========================================================
# ALCANCE ACADÉMICO
# =========================================================

st.divider()

st.caption(
    "Herramienta educativa basada en información local del proyecto. "
    "No sustituye la valoración profesional, las pruebas confirmatorias "
    "ni los lineamientos y protocolos oficiales."
)
