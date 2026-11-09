import html

import streamlit as st

from utils.state import initialize_state, load_diseases
from utils.theme import apply_theme, page_header


# =========================================================
# 1. CONFIGURACIÓN
# =========================================================

initialize_state()
apply_theme("epidemiologia")


# =========================================================
# 2. ESTILOS DEL MÓDULO
# =========================================================

st.markdown("""
<style>

/* INTRODUCCIÓN */

.epi-intro {
    color: var(--app-muted);
    font-size: 15px;
    line-height: 1.8;
    max-width: 900px;
    margin-bottom: 22px;
}

/* ETIQUETAS DE SECCIÓN */

.epi-label {
    color: var(--app-accent);
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 1.5px;
    margin-top: 6px;
    margin-bottom: 4px;
}

/* PANEL DE OBJETIVO */

.epi-context {
    background: #FFFFFF;
    border: 1px solid var(--app-border);
    border-left: 4px solid var(--app-accent);
    border-radius: 8px;
    padding: 18px 22px;
    margin: 12px 0 28px 0;
}

.epi-context strong {
    color: var(--app-primary);
    font-size: 16px;
}

.epi-description {
    color: #3F5459;
    font-size: 14px;
    line-height: 1.75;
}

.epi-context .epi-description {
    margin: 8px 0 0 0;
}

/* TARJETAS DE COMPARACIÓN */

.st-key-epi_dengue {
    border-top: 4px solid #3A6591 !important;
}

.st-key-epi_oropouche {
    border-top: 4px solid #2A7A69 !important;
}

.epi-disease-title {
    font-family: "Source Serif 4", Georgia, serif;
    font-size: 24px;
    font-weight: 700;
    margin: 4px 0 8px 0;
}

.epi-dengue {
    color: #3A6591;
}

.epi-oropouche {
    color: #2A7A69;
}

.epi-meta {
    margin-top: 14px;
}

.epi-meta-label {
    color: var(--app-muted);
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 1.3px;
    margin-bottom: 2px;
}

.epi-meta-value {
    color: var(--app-text);
    font-size: 14px;
    line-height: 1.6;
}

/* TARJETAS DE ENFERMEDADES */

.disease-name {
    font-family: "Source Serif 4", Georgia, serif;
    color: var(--app-primary);
    font-size: 21px;
    font-weight: 700;
    margin: 2px 0 6px 0;
}

.epi-chip {
    display: inline-block;
    background: #EAF2EF;
    color: var(--app-primary);
    border-radius: 999px;
    padding: 3px 12px;
    font-size: 12px;
    font-weight: 600;
    margin: 4px 0 10px 0;
}

</style>
""", unsafe_allow_html=True)


# =========================================================
# 3. ENCABEZADO
# =========================================================

page_header(
    "Vigilancia epidemiológica",
    "Panorama de las arbovirosis y otras enfermedades febriles "
    "de importancia para el diagnóstico diferencial en Colombia.",
    "MÓDULO 01 · EPIDEMIOLOGÍA"
)

st.markdown("""
<div class="epi-intro">
La vigilancia epidemiológica permite reconocer patrones de circulación
de enfermedades, identificar posibles brotes y orientar la investigación
de pacientes que presentan cuadros febriles similares.
</div>
""", unsafe_allow_html=True)


# =========================================================
# 4. OBJETIVO DEL MÓDULO
# =========================================================

st.markdown("""
<div class="epi-context">
    <div class="epi-label">OBJETIVO DE INVESTIGACIÓN</div>
    <strong>Reconocer el contexto epidemiológico de un caso clínico.</strong>
    <p class="epi-description">
    Analiza la ubicación geográfica, la exposición a vectores, los
    antecedentes de viaje y el tiempo de evolución para comprender
    qué información puede orientar un diagnóstico diferencial.
    </p>
</div>
""", unsafe_allow_html=True)


# =========================================================
# 5. COMPARACIÓN: DENGUE Y OROPOUCHE
# =========================================================

def meta_block(label, value):
    """Bloque pequeño de etiqueta + valor (solo con texto fijo del código)."""
    return (
        '<div class="epi-meta">'
        f'<div class="epi-meta-label">{label}</div>'
        f'<div class="epi-meta-value">{value}</div>'
        '</div>'
    )


st.markdown(
    '<div class="epi-label">COMPARACIÓN PRINCIPAL</div>',
    unsafe_allow_html=True
)

st.subheader("Dengue y Oropouche")

st.write(
    "Ambas enfermedades pueden producir cuadros febriles y compartir "
    "algunas manifestaciones clínicas. Sin embargo, presentan diferencias "
    "epidemiológicas que deben tenerse en cuenta durante la investigación."
)

col1, col2 = st.columns(2, gap="large")

with col1:

    with st.container(border=True, key="epi_dengue"):

        st.markdown(
            '<div class="epi-disease-title epi-dengue">Dengue</div>'
            '<div class="epi-description">'
            'Enfermedad viral causada por el virus del dengue y transmitida '
            'principalmente por mosquitos del género <i>Aedes</i>. '
            'Su circulación en Colombia hace que sea un diagnóstico '
            'prioritario ante determinados cuadros febriles.'
            '</div>'
            + meta_block("VECTOR PRINCIPAL", "Mosquitos del género <i>Aedes</i>")
            + meta_block(
                "ASPECTO PARA INVESTIGAR",
                "Antecedentes de exposición, signos de alarma y evolución clínica."
            ),
            unsafe_allow_html=True
        )

with col2:

    with st.container(border=True, key="epi_oropouche"):

        st.markdown(
            '<div class="epi-disease-title epi-oropouche">Oropouche</div>'
            '<div class="epi-description">'
            'Enfermedad viral causada por el virus Oropouche y transmitida '
            'principalmente por jejenes del género <i>Culicoides</i>. '
            'Sus manifestaciones pueden confundirse con las de otras '
            'arbovirosis.'
            '</div>'
            + meta_block("VECTOR PRINCIPAL", "Jejenes del género <i>Culicoides</i>")
            + meta_block(
                "ASPECTO PARA INVESTIGAR",
                "Exposición en zonas con circulación del virus y confirmación "
                "mediante pruebas de laboratorio."
            ),
            unsafe_allow_html=True
        )

st.divider()


# =========================================================
# 6. ENFERMEDADES DE LA INVESTIGACIÓN
# =========================================================

st.markdown(
    '<div class="epi-label">BASE DE CONOCIMIENTO</div>',
    unsafe_allow_html=True
)

st.subheader("Arbovirosis incluidas en la investigación")

st.write(
    "Consulta las enfermedades registradas en la base científica "
    "del simulador y revisa sus principales características."
)


def format_information(value):
    """Convierte información del JSON en una lista Markdown legible."""

    if value is None:
        return "Información no especificada."

    if isinstance(value, list):

        if not value:
            return "Información no especificada."

        return "\n".join(f"- {item}" for item in value)

    if isinstance(value, dict):

        if not value:
            return "Información no especificada."

        return "\n".join(
            f"- **{key.replace('_', ' ').capitalize()}:** {item}"
            for key, item in value.items()
        )

    return str(value)


diseases = load_diseases()

if not isinstance(diseases, dict):
    diseases = {}

arboviruses = {
    key: value
    for key, value in diseases.items()
    if (
        isinstance(value, dict)
        and str(value.get("categoria", "")).strip().casefold()
        == "arbovirosis"
    )
}

if arboviruses:

    disease_items = list(arboviruses.items())

    st.caption(
        f"{len(disease_items)} enfermedades registradas en esta categoría."
    )

    for start in range(0, len(disease_items), 2):

        columns = st.columns(2, gap="large")

        for column, (key, disease) in zip(
            columns,
            disease_items[start:start + 2]
        ):

            with column:

                with st.container(border=True):

                    disease_name = disease.get("nombre", key)
                    agent = disease.get("agente", "No especificado")

                    st.markdown(
                        f'<div class="disease-name">'
                        f'{html.escape(str(disease_name))}</div>',
                        unsafe_allow_html=True
                    )

                    st.markdown(
                        f'<span class="epi-chip">'
                        f'Agente: {html.escape(str(agent))}</span>',
                        unsafe_allow_html=True
                    )

                    st.write(
                        disease.get(
                            "descripcion",
                            "No hay una descripción disponible."
                        )
                    )

                    with st.expander(
                        f"Consultar información de {disease_name}"
                    ):

                        st.markdown("**Vector**")
                        st.write(
                            disease.get(
                                "vector",
                                "Información no especificada."
                            )
                        )

                        st.markdown("**Manifestaciones clínicas**")
                        st.markdown(
                            format_information(
                                disease.get("manifestaciones")
                            )
                        )

                        st.markdown("**Pistas epidemiológicas**")
                        st.markdown(
                            format_information(
                                disease.get("pistas")
                            )
                        )

                        st.markdown("**Pruebas diagnósticas**")
                        st.markdown(
                            format_information(
                                disease.get("pruebas")
                            )
                        )

                        st.markdown("**Consideraciones**")
                        st.markdown(
                            format_information(
                                disease.get("consideraciones")
                            )
                        )

else:

    st.warning(
        "No se encontraron enfermedades clasificadas como "
        "arbovirosis en el archivo data/enfermedades.json. "
        "Verifica el campo categoria de los registros."
    )


st.divider()


# =========================================================
# 7. FACTORES EPIDEMIOLÓGICOS
# =========================================================

st.markdown(
    '<div class="epi-label">ANÁLISIS DEL CONTEXTO</div>',
    unsafe_allow_html=True
)

st.subheader("Factores que orientan la investigación")

st.write(
    "Selecciona un factor para conocer su importancia al estudiar "
    "un paciente con síndrome febril."
)

explanations = {

    "Ubicación geográfica": (
        "La región donde vive o estuvo el paciente permite identificar "
        "qué enfermedades pueden circular en esa zona. También ayuda "
        "a orientar las preguntas sobre lugares de exposición."
    ),

    "Exposición a vectores": (
        "El contacto con ambientes donde existen mosquitos o jejenes "
        "aporta información relevante. Sin embargo, una picadura "
        "no confirma por sí sola una infección."
    ),

    "Días de evolución": (
        "El tiempo transcurrido desde el inicio de los síntomas influye "
        "en la selección y la interpretación de las pruebas diagnósticas. "
        "La utilidad de cada prueba depende de su ventana diagnóstica."
    ),

    "Circulación de enfermedades": (
        "Los reportes de vigilancia permiten conocer qué enfermedades "
        "se han identificado en una región y contextualizar los casos. "
        "La información debe corresponder al periodo investigado."
    ),

    "Antecedentes de viaje": (
        "Los lugares visitados y las fechas de desplazamiento permiten "
        "identificar posibles exposiciones antes del inicio de los síntomas."
    )
}

factor = st.selectbox(
    "Factor epidemiológico",
    options=list(explanations.keys()),
    index=0
)

with st.container(border=True):

    st.markdown(f"**{factor}**")
    st.write(explanations[factor])


# =========================================================
# 8. CONOCIMIENTO CLAVE
# =========================================================

st.divider()

st.markdown(
    '<div class="epi-label">CONCEPTO FUNDAMENTAL</div>',
    unsafe_allow_html=True
)

st.subheader("La fiebre no es suficiente para diferenciar")

st.write(
    "La fiebre, la cefalea y las mialgias pueden aparecer en diferentes "
    "enfermedades infecciosas. Por esta razón, no deben utilizarse de "
    "manera aislada para confirmar dengue u Oropouche."
)

st.warning(
    "El diagnóstico diferencial requiere integrar antecedentes, "
    "contexto epidemiológico, evolución clínica y pruebas de laboratorio. "
    "La presencia de signos de alarma exige valoración clínica oportuna."
)


# =========================================================
# 9. ALCANCE DE LA INFORMACIÓN
# =========================================================

st.divider()

st.caption("ALCANCE DEL MÓDULO")

st.write(
    "Esta sección presenta información académica general. "
    "No constituye un sistema de vigilancia en tiempo real ni "
    "representa cifras epidemiológicas actualizadas."
)

st.caption("OPERACIÓN OROPOUCHE · SIMULADOR EDUCATIVO · COLOMBIA")

st.caption(
    "Los escenarios y resultados de los pacientes son simulados. "
    "El diagnóstico y la vigilancia reales deben seguir los lineamientos "
    "vigentes de las autoridades sanitarias."
)