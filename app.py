
import streamlit as st

from utils.state import (
    initialize_state,
    load_cases,
    get_score,
    get_progress,
    get_completed_count,
    get_total_cases
)

from utils.theme import apply_theme


# =========================================================
# 1. CONFIGURACIÓN GENERAL
# =========================================================

st.set_page_config(
    page_title="Operación Oropouche | Centro de investigación",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded"
)

initialize_state()
apply_theme("inicio")


# =========================================================
# 2. ESTILOS DE LA PORTADA
# =========================================================

st.markdown("""
<style>

/* PORTADA PRINCIPAL */

.st-key-home_hero {
    background:
        radial-gradient(
            circle at 90% 15%,
            rgba(111, 171, 153, 0.25),
            transparent 30%
        ),
        linear-gradient(
            112deg,
            #142F3A 0%,
            #1B4550 65%,
            #245B5D 100%
        );
    border-radius: 12px;
    padding: 35px 38px;
    border-bottom: 4px solid #398E7D;
    margin-bottom: 28px;
}

.st-key-home_hero h1 {
    color: #FFFFFF !important;
    font-size: clamp(32px, 4vw, 46px) !important;
    line-height: 1.15 !important;
    font-weight: 850 !important;
    margin-top: 8px;
    margin-bottom: 15px;
}

.st-key-home_hero p {
    color: #E0EBE8 !important;
    font-size: 15px;
    line-height: 1.8;
}

.st-key-home_hero [data-testid="stCaptionContainer"] p {
    color: #A9D6CA !important;
    font-size: 11px;
    font-weight: 800;
    letter-spacing: 1.8px;
}

.st-key-home_hero hr {
    border-color: rgba(255,255,255,0.18);
}

/* BOTÓN PRINCIPAL DE PORTADA */

.st-key-home_hero .stButton > button {
    background: #A9D6CA;
    color: #173C43;
    border: 1px solid #A9D6CA;
    border-radius: 7px;
    font-weight: 800;
    min-height: 46px;
}

.st-key-home_hero .stButton > button:hover {
    background: #FFFFFF;
    color: #173C43;
    border-color: #FFFFFF;
}

/* TÍTULOS DE SECCIÓN */

.home-section-label {
    color: #398E7D;
    font-size: 11px;
    font-weight: 850;
    letter-spacing: 1.5px;
    margin-bottom: 5px;
}

.home-section-description {
    color: #607278;
    font-size: 13px;
    margin-top: -8px;
    margin-bottom: 18px;
}

/* IDENTIDAD DE LA BARRA LATERAL */

.sidebar-brand {
    padding: 10px 0 19px 0;
    border-bottom: 1px solid #DCE4E1;
    margin-bottom: 16px;
}

.sidebar-brand-title {
    color: #1B4550;
    font-size: 17px;
    font-weight: 900;
    letter-spacing: 0.3px;
}

.sidebar-brand-subtitle {
    color: #607278;
    font-size: 9px;
    font-weight: 800;
    letter-spacing: 1.4px;
    margin-top: 5px;
}

/* BOTONES DE NAVEGACIÓN */

[data-testid="stSidebar"] .stButton > button {
    text-align: left;
    justify-content: flex-start;
    background: transparent;
    color: #29434A;
    border: 1px solid transparent;
    border-radius: 7px;
    font-weight: 650;
    min-height: 39px;
    padding-left: 12px;
}

[data-testid="stSidebar"] .stButton > button:hover {
    background: #EAF2EF;
    color: #1B655A;
    border-color: #D7E7E0;
}

/* MÓDULOS */

.module-number {
    color: #398E7D;
    font-size: 11px;
    font-weight: 850;
    letter-spacing: 1.3px;
}

.module-description {
    color: #607278;
    font-size: 13px;
    line-height: 1.65;
    min-height: 43px;
}

/* BOTONES DE MÓDULOS */

.module-button .stButton > button {
    border-radius: 7px;
    min-height: 40px;
}

/* EXPEDIENTE ACTIVO */

.st-key-active_case_panel {
    background: #FFFFFF;
    border-left: 4px solid #398E7D;
    border-radius: 7px;
    padding: 15px 20px;
}

/* PIE DE PÁGINA */

.home-footer {
    color: #607278;
    font-size: 11px;
    line-height: 1.8;
    text-align: center;
    padding: 15px 0 5px 0;
}

/* AJUSTES RESPONSIVE */

@media (max-width: 768px) {
    .st-key-home_hero {
        padding: 23px 20px;
    }

    .st-key-home_hero h1 {
        font-size: 31px !important;
    }
}

</style>
""", unsafe_allow_html=True)


# =========================================================
# 3. DATOS DE LA INVESTIGACIÓN
# =========================================================

cases = load_cases()

if not isinstance(cases, dict):
    cases = {}

total_cases = get_total_cases()
completed = get_completed_count()
score = get_score()

progress = max(
    0,
    min(100, get_progress() * 100)
)

user_name = st.session_state.get(
    "user_name",
    "Investigador"
)

if not user_name or not user_name.strip():
    user_name = "Investigador"


# =========================================================
# 4. NAVEGACIÓN
# =========================================================

modules = [
    (
        "01",
        "Inteligencia epidemiológica",
        "Estudia la circulación de arbovirus, vectores y contexto epidemiológico.",
        "pages/1_Epidemiologia.py"
    ),
    (
        "02",
        "Biblioteca científica",
        "Consulta agentes etiológicos, manifestaciones clínicas y diferencias.",
        "pages/2_Base_Cientifica.py"
    ),
    (
        "03",
        "Expedientes clínicos",
        "Analiza pacientes, síntomas, antecedentes y factores de exposición.",
        "pages/3_Pacientes.py"
    ),
    (
        "04",
        "Laboratorio",
        "Solicita pruebas diagnósticas y analiza los resultados simulados.",
        "pages/4_Laboratorio.py"
    ),
    (
        "05",
        "Asistente educativo",
        "Consulta conceptos y resuelve dudas sobre las enfermedades estudiadas.",
        "pages/5_Asistente_IA.py"
    ),
    (
        "06",
        "Desafíos médicos",
        "Resuelve los casos y justifica tus decisiones diagnósticas.",
        "pages/6_Desafios.py"
    ),
    (
        "07",
        "Resultados y evaluación",
        "Revisa tu puntuación, progreso e historial de investigaciones.",
        "pages/7_Resultados.py"
    )
]


# =========================================================
# 5. BARRA LATERAL
# =========================================================

with st.sidebar:

    st.markdown("""
    <div class="sidebar-brand">
        <div class="sidebar-brand-title">
            OPERACIÓN OROPOUCHE
        </div>
        <div class="sidebar-brand-subtitle">
            INVESTIGACIÓN EN SALUD PÚBLICA
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.caption("PERFIL DEL INVESTIGADOR")

    new_name = st.text_input(
        "Nombre del investigador",
        value=user_name,
        placeholder="Escribe tu nombre",
        label_visibility="collapsed",
        key="user_name_input"
    )

    if new_name.strip():
        st.session_state.user_name = new_name.strip()

    st.caption("Investigador en formación")

    st.divider()

    st.caption("NAVEGACIÓN PRINCIPAL")

    for number, title, description, path in modules:

        if st.button(
            title,
            key=f"sidebar_{number}",
            use_container_width=True
        ):
            st.switch_page(path)

    st.divider()

    st.caption("ESTADO DE INVESTIGACIÓN")

    st.write(
        f"Expedientes resueltos: {completed} de {total_cases}"
    )

    st.progress(progress / 100)

    st.write(f"Puntuación acumulada: **{score} puntos**")

    st.divider()

    st.caption("Proyecto académico · Colombia")
    st.caption("Casos y resultados simulados.")


# =========================================================
# 6. PORTADA PRINCIPAL
# =========================================================

with st.container(key="home_hero"):

    st.caption(
        "CENTRO DE INVESTIGACIÓN EPIDEMIOLÓGICA"
    )

    st.title("El retorno de Oropouche")

    st.write(
        f"Bienvenido, {st.session_state.user_name}. "
        "Investiga los casos clínicos, analiza la evidencia "
        "de laboratorio y estudia los desafíos del diagnóstico "
        "diferencial frente al dengue endémico en Colombia."
    )

    st.divider()

    st.caption(
        "PLATAFORMA ACADÉMICA · VIGILANCIA · "
        "INVESTIGACIÓN · DIAGNÓSTICO DIFERENCIAL"
    )

    if st.button(
        "Comenzar investigación",
        key="start_investigation",
        use_container_width=False
    ):
        st.switch_page("pages/3_Pacientes.py")


# =========================================================
# 7. RESUMEN DE INVESTIGACIÓN
# =========================================================

st.markdown(
    '<div class="home-section-label">SEGUIMIENTO</div>',
    unsafe_allow_html=True
)

st.subheader("Resumen de investigación")

st.markdown(
    '<div class="home-section-description">'
    'Consulta el estado actual de tu actividad en la plataforma.'
    '</div>',
    unsafe_allow_html=True
)

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.metric(
        "Expedientes resueltos",
        f"{completed}/{total_cases}"
    )

with c2:
    st.metric(
        "Puntuación acumulada",
        score
    )

with c3:
    st.metric(
        "Progreso general",
        f"{progress:.0f}%"
    )

with c4:

    status = (
        "Finalizada"
        if total_cases > 0 and completed >= total_cases
        else "En curso"
    )

    st.metric(
        "Estado",
        status
    )

st.progress(progress / 100)


# =========================================================
# 8. INVESTIGACIÓN ACTUAL
# =========================================================

st.markdown(
    '<div class="home-section-label">EXPEDIENTES</div>',
    unsafe_allow_html=True
)

st.subheader("Investigación en curso")

st.markdown(
    '<div class="home-section-description">'
    'Retoma el expediente activo o comienza una nueva evaluación.'
    '</div>',
    unsafe_allow_html=True
)

active_case_id = st.session_state.get("active_case_id")

if active_case_id and active_case_id in cases:

    active_case = cases[active_case_id]

    case_title = active_case.get(
        "titulo",
        "Expediente clínico activo"
    )

    with st.container(key="active_case_panel"):

        st.caption("EXPEDIENTE ACTIVO")

        st.markdown(f"**{case_title}**")

        st.write(
            "Continúa revisando los antecedentes, los hallazgos "
            "clínicos y las pruebas diagnósticas de este expediente."
        )

        if st.button(
            "Continuar con el expediente",
            key="continue_active_case"
        ):
            st.switch_page("pages/3_Pacientes.py")

else:

    st.write(
        "Todavía no tienes un expediente activo. "
        "Puedes comenzar revisando los casos clínicos disponibles."
    )

    if st.button(
        "Consultar expedientes clínicos",
        key="open_patient_files"
    ):
        st.switch_page("pages/3_Pacientes.py")


# =========================================================
# 9. ÁREAS DE INVESTIGACIÓN
# =========================================================

st.markdown(
    '<div class="home-section-label">PLATAFORMA</div>',
    unsafe_allow_html=True
)

st.subheader("Áreas de investigación")

st.markdown(
    '<div class="home-section-description">'
    'Accede a las diferentes herramientas de análisis y aprendizaje.'
    '</div>',
    unsafe_allow_html=True
)

for start in range(0, len(modules), 2):

    columns = st.columns(2)

    for col, module in zip(
        columns,
        modules[start:start + 2]
    ):

        number, title, description, path = module

        with col:

            st.markdown(
                f'<div class="module-number">ÁREA {number}</div>',
                unsafe_allow_html=True
            )

            st.markdown(f"### {title}")

            st.markdown(
                f'<div class="module-description">'
                f'{description}'
                f'</div>',
                unsafe_allow_html=True
            )

            st.write("")

            if st.button(
                "Ingresar al módulo",
                key=f"open_module_{number}",
                use_container_width=True
            ):
                st.switch_page(path)

            st.write("")


# =========================================================
# 10. METODOLOGÍA DE INVESTIGACIÓN
# =========================================================

st.markdown(
    '<div class="home-section-label">METODOLOGÍA</div>',
    unsafe_allow_html=True
)

st.subheader("Etapas de la investigación")

st.markdown(
    '<div class="home-section-description">'
    'Conoce el procedimiento que debes seguir durante cada caso clínico.'
    '</div>',
    unsafe_allow_html=True
)

with st.expander("Consultar las etapas de la investigación"):

    steps = [
        (
            "01. Revisión del expediente",
            "Estudia los datos del paciente, sus antecedentes y el motivo de consulta."
        ),
        (
            "02. Análisis clínico y epidemiológico",
            "Identifica síntomas, signos de alarma y factores de exposición."
        ),
        (
            "03. Selección de pruebas",
            "Solicita las pruebas de laboratorio pertinentes para el escenario."
        ),
        (
            "04. Interpretación de resultados",
            "Compara los hallazgos con las características de las enfermedades."
        ),
        (
            "05. Diagnóstico diferencial",
            "Selecciona una respuesta y revisa la retroalimentación del caso."
        )
    ]

    for title, description in steps:

        st.markdown(f"**{title}**")
        st.write(description)


# =========================================================
# 11. PIE DE PÁGINA
# =========================================================

st.divider()

st.markdown("""
<div class="home-footer">
    <strong>OPERACIÓN OROPOUCHE</strong><br>
    Proyecto académico de diagnóstico diferencial en arbovirosis.<br>
    Los pacientes y resultados son simulados con fines educativos.<br>
    Esta plataforma no sustituye la valoración médica ni los protocolos clínicos oficiales.
</div>
""", unsafe_allow_html=True)
