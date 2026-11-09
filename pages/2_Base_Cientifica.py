
import streamlit as st

from utils.state import initialize_state, load_diseases
from utils.theme import apply_theme, page_header


# =========================================================
# 1. CONFIGURACIÓN
# =========================================================

initialize_state()
apply_theme("ciencia")


# =========================================================
# 2. ESTILOS DEL MÓDULO
# =========================================================

st.markdown("""
<style>

/* INTRODUCCIÓN */

.science-intro {
    color: #617184;
    font-size: 14px;
    line-height: 1.8;
    max-width: 900px;
    margin-bottom: 20px;
}

/* ETIQUETAS */

.science-label {
    color: #6686AA;
    font-size: 11px;
    font-weight: 850;
    letter-spacing: 1.5px;
    margin-bottom: 5px;
}

/* DATOS PRINCIPALES */

.science-data-label {
    color: #617184;
    font-size: 10px;
    font-weight: 850;
    letter-spacing: 1px;
    text-transform: uppercase;
    margin-bottom: 5px;
}

.science-data-value {
    color: #26384D;
    font-size: 14px;
    line-height: 1.7;
}

/* ENFERMEDAD SELECCIONADA */

.science-feature {
    background: #FFFFFF;
    border-left: 4px solid #6686AA;
    border-radius: 6px;
    padding: 18px 21px;
    margin: 15px 0 24px 0;
}

/* COMPARACIÓN */

.science-comparison {
    background: #FFFFFF;
    border-top: 3px solid #6686AA;
    border-radius: 6px;
    padding: 15px;
}

/* TEXTO SECUNDARIO */

.science-muted {
    color: #617184;
    font-size: 12px;
    line-height: 1.7;
}

</style>
""", unsafe_allow_html=True)


# =========================================================
# 3. FUNCIONES AUXILIARES
# =========================================================

def get_text(value, fallback="Información no disponible."):
    """Convierte un valor del JSON en texto legible."""

    if value is None or value == "":
        return fallback

    if isinstance(value, list):
        if not value:
            return fallback

        return "\n".join(f"• {item}" for item in value)

    if isinstance(value, dict):
        if not value:
            return fallback

        return "\n".join(
            f"• {key.replace('_', ' ').capitalize()}: {item}"
            for key, item in value.items()
        )

    return str(value)


def get_items(value):
    """Normaliza listas y textos para mostrarlos como elementos."""

    if value is None or value == "":
        return []

    if isinstance(value, list):
        return value

    if isinstance(value, dict):
        return [
            f"{key.replace('_', ' ').capitalize()}: {item}"
            for key, item in value.items()
        ]

    return [value]


def show_list(title, values, empty_message="No hay información registrada."):
    """Presenta una lista de información científica."""

    st.markdown(f"**{title}**")

    items = get_items(values)

    if not items:
        st.caption(empty_message)
        return

    for item in items:
        st.markdown(f"- {item}")


def disease_name(key):
    """Obtiene el nombre legible de una enfermedad."""

    return diseases[key].get("nombre", key)


# =========================================================
# 4. ENCABEZADO
# =========================================================

page_header(
    "Biblioteca científica",
    "Consulta las características de las enfermedades incluidas "
    "en la investigación y reconoce sus diferencias clínicas y diagnósticas.",
    "MÓDULO 02 · BASE CIENTÍFICA"
)

st.markdown("""
<div class="science-intro">
Esta biblioteca reúne información sobre agentes etiológicos,
mecanismos de transmisión, manifestaciones clínicas y pruebas
diagnósticas. Su propósito es apoyar el análisis diferencial
de los escenarios clínicos del simulador.
</div>
""", unsafe_allow_html=True)


# =========================================================
# 5. CARGA DE ENFERMEDADES
# =========================================================

diseases = load_diseases()

if not isinstance(diseases, dict) or not diseases:

    st.error(
        "No fue posible cargar las enfermedades. "
        "Verifica el contenido de data/enfermedades.json."
    )

    st.stop()


# =========================================================
# 6. SELECCIÓN DE ENFERMEDAD
# =========================================================

st.markdown(
    '<div class="science-label">CONSULTA DE ENFERMEDADES</div>',
    unsafe_allow_html=True
)

st.subheader("Selecciona una enfermedad")

st.write(
    "Elige una enfermedad para consultar su información "
    "y revisar los elementos que orientan su diagnóstico."
)

disease_ids = list(diseases.keys())

disease_id = st.selectbox(
    "Enfermedad",
    options=disease_ids,
    format_func=disease_name,
    key="science_disease_selector"
)

disease = diseases[disease_id]


# =========================================================
# 7. INFORMACIÓN GENERAL
# =========================================================

st.divider()

st.markdown(
    '<div class="science-label">FICHA DE REFERENCIA</div>',
    unsafe_allow_html=True
)

st.title(disease.get("nombre", disease_id))

st.caption(
    disease.get("categoria", "Categoría no especificada")
)

st.write(
    disease.get(
        "descripcion",
        "No hay una descripción disponible para esta enfermedad."
    )
)


# =========================================================
# 8. AGENTE Y TRANSMISIÓN
# =========================================================

st.markdown(
    '<div class="science-label">CARACTERÍSTICAS BIOLÓGICAS</div>',
    unsafe_allow_html=True
)

st.subheader("Agente etiológico y transmisión")

col1, col2 = st.columns(2, gap="large")

with col1:

    st.markdown("**Agente etiológico**")

    st.write(
        disease.get(
            "agente",
            "Información no especificada."
        )
    )

with col2:

    st.markdown("**Vector o vía de transmisión**")

    st.write(
        disease.get(
            "vector",
            "Información no especificada."
        )
    )


# =========================================================
# 9. MANIFESTACIONES Y PISTAS
# =========================================================

st.divider()

st.markdown(
    '<div class="science-label">EVALUACIÓN CLÍNICA</div>',
    unsafe_allow_html=True
)

st.subheader("Manifestaciones clínicas y diagnóstico diferencial")

col1, col2 = st.columns(2, gap="large")

with col1:

    show_list(
        "Manifestaciones clínicas",
        disease.get("manifestaciones")
    )

with col2:

    show_list(
        "Pistas para el diagnóstico diferencial",
        disease.get("pistas")
    )


# =========================================================
# 10. PRUEBAS DIAGNÓSTICAS
# =========================================================

st.divider()

st.markdown(
    '<div class="science-label">APOYO DIAGNÓSTICO</div>',
    unsafe_allow_html=True
)

st.subheader("Pruebas diagnósticas relacionadas")

tests = get_items(disease.get("pruebas"))

if tests:

    for test in tests:
        st.markdown(f"- {test}")

else:

    st.caption(
        "No se registraron pruebas diagnósticas para esta enfermedad."
    )


# =========================================================
# 11. CONSIDERACIONES
# =========================================================

st.divider()

st.markdown(
    '<div class="science-label">CONSIDERACIONES CLÍNICAS</div>',
    unsafe_allow_html=True
)

st.subheader("Aspectos que debes tener en cuenta")

considerations = disease.get(
    "consideraciones",
    "No hay consideraciones adicionales registradas."
)

st.info(get_text(considerations))


# =========================================================
# 12. COMPARACIÓN DE ENFERMEDADES
# =========================================================

st.divider()

st.markdown(
    '<div class="science-label">ANÁLISIS COMPARATIVO</div>',
    unsafe_allow_html=True
)

st.subheader("Comparar enfermedades")

st.write(
    "Selecciona hasta tres enfermedades para contrastar "
    "sus manifestaciones clínicas y pruebas diagnósticas."
)

selected = st.multiselect(
    "Enfermedades para comparar",
    options=disease_ids,
    default=[disease_id],
    max_selections=3,
    format_func=disease_name,
    key="science_comparison_selector"
)

if selected:

    comparison_columns = st.columns(
        len(selected),
        gap="medium"
    )

    for column, key in zip(comparison_columns, selected):

        item = diseases[key]

        with column:

            st.markdown(
                f'<div class="science-label">'
                f'{item.get("categoria", "ENFERMEDAD").upper()}'
                f'</div>',
                unsafe_allow_html=True
            )

            st.markdown(f"### {item.get('nombre', key)}")

            st.markdown("**Agente**")

            st.write(
                item.get(
                    "agente",
                    "No especificado."
                )
            )

            st.divider()

            show_list(
                "Manifestaciones principales",
                get_items(item.get("manifestaciones"))[:5]
            )

            st.divider()

            show_list(
                "Pruebas diagnósticas",
                item.get("pruebas")
            )

            st.divider()

            show_list(
                "Pistas diferenciales",
                item.get("pistas")
            )

else:

    st.caption(
        "Selecciona al menos una enfermedad para iniciar la comparación."
    )


# =========================================================
# 13. MENSAJE DE SEGURIDAD
# =========================================================

st.divider()

st.markdown(
    '<div class="science-label">INTERPRETACIÓN RESPONSABLE</div>',
    unsafe_allow_html=True
)

st.warning(
    "Las manifestaciones clínicas pueden superponerse entre "
    "diferentes enfermedades. Las características presentadas "
    "orientan la investigación, pero no confirman por sí solas "
    "un diagnóstico. La interpretación debe considerar el contexto "
    "epidemiológico, la evolución clínica y las pruebas pertinentes."
)


# =========================================================
# 14. PIE DE MÓDULO
# =========================================================

st.divider()

st.caption(
    "OPERACIÓN OROPOUCHE · BIBLIOTECA CIENTÍFICA"
)

st.caption(
    "Contenido académico de consulta. Para la práctica clínica "
    "deben utilizarse las recomendaciones y protocolos vigentes "
    "de las autoridades sanitarias."
)
