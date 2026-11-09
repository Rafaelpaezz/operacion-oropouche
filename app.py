from pathlib import Path

import streamlit as st

from utils.state import (
    initialize_state,
    load_cases,
    get_score,
    get_progress,
    get_completed_count,
    get_total_cases
)

from utils.theme import apply_theme, MODULE_COLORS


# =========================================================
# 0. IMÁGENES E ÍCONOS
#    Si una foto no existe en assets/, la tarjeta usa un ícono.
#    Nada se rompe si faltan imágenes.
# =========================================================

BASE_DIR = Path(__file__).parent
ASSETS = BASE_DIR / "assets"


def find_image(name):
    """Busca assets/<name>.(jpg|jpeg|png|webp) y devuelve la ruta o None."""
    for ext in ("jpg", "jpeg", "png", "webp"):
        path = ASSETS / f"{name}.{ext}"
        if path.exists():
            return str(path)
    return None


_SVG_OPEN = (
    '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" '
    'fill="none" stroke="currentColor" stroke-width="1.5" '
    'stroke-linecap="round" stroke-linejoin="round">'
)

ICONS = {
    "01": '<circle cx="12" cy="12" r="9"/><ellipse cx="12" cy="12" rx="4" ry="9"/>'
          '<path d="M3 12h18"/>',
    "02": '<path d="M5 4h10a4 4 0 0 1 4 4v12H9a4 4 0 0 1-4-4z"/><path d="M9 8h6M9 12h6"/>',
    "03": '<rect x="5" y="4" width="14" height="17" rx="2"/>'
          '<rect x="9" y="2" width="6" height="4" rx="1"/><path d="M8 11h8M8 15h8"/>',
    "04": '<path d="M9 3h6M10 3v6l-5 10a2 2 0 0 0 2 3h10a2 2 0 0 0 2-3l-5-10V3"/>'
          '<path d="M7.5 15h9"/>',
    "05": '<path d="M4 5h16v11H9l-5 4z"/><path d="M8 9h8M8 12h5"/>',
    "06": '<circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="5"/>'
          '<circle cx="12" cy="12" r="1.2"/>',
    "07": '<path d="M4 20h16"/><path d="M6 20v-7M12 20V5M18 20v-10"/>',
}


def icon_svg(number):
    return _SVG_OPEN + ICONS.get(number, "") + "</svg>"


# =========================================================
# 1. CONFIGURACIÓN GENERAL
# =========================================================

st.set_page_config(
    page_title="Operación Oropouche | Centro de investigación",
    page_icon=find_image("favicon") or "🩺",
    layout="wide",
    initial_sidebar_state="expanded"
)

initialize_state()
apply_theme("inicio")   # también dibuja la barra lateral compartida


# =========================================================
# 2. ESTILOS PROPIOS DE LA PORTADA
#    (botones, métricas, barra lateral y colores base viven en theme.py)
# =========================================================

st.markdown("""
<style>

/* ---------- PORTADA ---------- */

.st-key-home_hero {
    background: linear-gradient(115deg, #12394A 0%, #17323A 55%, #0B7A6E 170%);
    border-radius: 14px;
    padding: 40px 42px;
    border-bottom: 4px solid var(--app-accent);
    margin-bottom: 32px;
}

.st-key-home_hero h1 {
    color: #FFFFFF !important;
    font-size: clamp(32px, 4vw, 46px) !important;
    line-height: 1.12 !important;
    font-weight: 700 !important;
    margin: 8px 0 16px 0;
}

.st-key-home_hero p {
    color: #E0EBE8 !important;
    font-size: 15px;
    line-height: 1.8;
}

.st-key-home_hero [data-testid="stCaptionContainer"] p {
    color: #A9D6CA !important;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 1.8px;
}

.st-key-home_hero hr {
    border-color: rgba(255,255,255,0.18);
}

.st-key-home_hero img {
    border-radius: 12px;
    height: 330px;
    object-fit: cover;
    box-shadow: 0 14px 34px rgba(0,0,0,0.35);
}

/* Botón principal de la portada: menta con texto oscuro */
.st-key-home_hero .stButton > button {
    background: #A9D6CA;
    color: #173C43;
    border: 1px solid #A9D6CA;
    font-weight: 700;
    min-height: 46px;
    padding: 0 28px;
}

.st-key-home_hero .stButton > button:hover {
    background: #FFFFFF;
    border-color: #FFFFFF;
    color: #173C43;
}

/* ---------- TÍTULOS DE SECCIÓN ---------- */

.home-section-label {
    color: var(--app-accent);
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 1.5px;
    margin-top: 18px;
    margin-bottom: 4px;
}

.home-section-description {
    color: var(--app-muted);
    font-size: 13px;
    margin-top: -8px;
    margin-bottom: 20px;
}

/* ---------- TARJETAS DE MÓDULOS ---------- */

[class*="st-key-card_"] {
    background: #FFFFFF;
    border: 1px solid var(--app-border) !important;
    border-radius: 12px;
    padding: 0;
    gap: 0.35rem;
    overflow: hidden;
    transition: box-shadow .2s ease, transform .2s ease, border-color .2s ease;
}

[class*="st-key-card_"]:hover {
    box-shadow: 0 10px 26px rgba(20,47,58,0.14);
    transform: translateY(-2px);
}

[class*="st-key-card_"] img {
    height: 150px;
    object-fit: cover;
    border-radius: 0;
    width: 100%;
}

/* Banda con ícono cuando la tarjeta no tiene foto
   (el color de fondo se define en línea, por módulo) */
.card-icon-band {
    height: 110px;
    display: flex;
    align-items: center;
    padding: 0 22px;
}

.card-icon-band svg {
    width: 44px;
    height: 44px;
    color: #FFFFFF;
}

.card-icon-band .band-number {
    margin-left: auto;
    color: rgba(255,255,255,0.30);
    font-size: 42px;
    font-weight: 700;
    letter-spacing: -1px;
    font-family: "Source Serif 4", Georgia, serif;
}

.card-body {
    padding: 8px 18px 0 18px;
}

.module-number {
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 1.3px;
}

.module-title {
    color: var(--app-primary);
    font-family: "Source Serif 4", Georgia, serif;
    font-size: 19px;
    font-weight: 700;
    line-height: 1.25;
    margin: 4px 0 6px 0;
}

.module-description {
    color: var(--app-muted);
    font-size: 13.5px;
    line-height: 1.6;
    min-height: 62px;
}

/* Margen lateral para que el botón no toque los bordes */
[class*="st-key-card_"] .stButton {
    padding: 0 18px 18px 18px;
}

/* ---------- EXPEDIENTE ACTIVO ---------- */

.st-key-active_case_panel {
    background: #FFFFFF;
    border: 1px solid var(--app-border);
    border-left: 4px solid var(--app-accent);
    border-radius: 8px;
    padding: 18px 22px;
}

/* ---------- ETAPAS ---------- */

.step-item {
    display: flex;
    gap: 14px;
    align-items: flex-start;
    padding: 12px 0;
    border-bottom: 1px solid #E8EEEC;
}

.step-num {
    flex: 0 0 34px;
    height: 34px;
    border-radius: 50%;
    background: var(--app-accent-soft);
    color: var(--app-accent);
    font-weight: 700;
    font-size: 13px;
    display: flex;
    align-items: center;
    justify-content: center;
}

.step-title { color: var(--app-primary); font-weight: 700; font-size: 14px; }
.step-desc  { color: var(--app-muted); font-size: 13px; margin-top: 2px; }

/* ---------- PIE ---------- */

.home-footer {
    color: var(--app-muted);
    font-size: 11px;
    line-height: 1.8;
    text-align: center;
    padding: 15px 0 5px 0;
}

@media (max-width: 768px) {
    .st-key-home_hero { padding: 24px 20px; }
    .st-key-home_hero h1 { font-size: 31px !important; }
    .st-key-home_hero img { height: 200px; margin-top: 14px; }
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

progress = max(0, min(100, get_progress() * 100))

user_name = st.session_state.get("user_name", "Investigador")

if not user_name or not user_name.strip():
    user_name = "Investigador"


# =========================================================
# 4. MÓDULOS
#    (número, título, descripción, página, nombre de imagen)
# =========================================================

modules = [
    ("01", "Inteligencia epidemiológica",
     "Estudia la circulación de arbovirus, vectores y contexto epidemiológico.",
     "pages/1_Epidemiologia.py", "mod_01_epidemiologia"),
    ("02", "Biblioteca científica",
     "Consulta agentes etiológicos, manifestaciones clínicas y diferencias.",
     "pages/2_Base_Cientifica.py", "mod_02_biblioteca"),
    ("03", "Expedientes clínicos",
     "Analiza pacientes, síntomas, antecedentes y factores de exposición.",
     "pages/3_Pacientes.py", "mod_03_expedientes"),
    ("04", "Laboratorio",
     "Solicita pruebas diagnósticas y analiza los resultados simulados.",
     "pages/4_Laboratorio.py", "mod_04_laboratorio"),
    ("05", "Asistente educativo",
     "Consulta conceptos y resuelve dudas sobre las enfermedades estudiadas.",
     "pages/5_Asistente_IA.py", "mod_05_asistente"),
    ("06", "Desafíos médicos",
     "Resuelve los casos y justifica tus decisiones diagnósticas.",
     "pages/6_Desafios.py", "mod_06_desafios"),
    ("07", "Resultados y evaluación",
     "Revisa tu puntuación, progreso e historial de investigaciones.",
     "pages/7_Resultados.py", "mod_07_resultados"),
]


# =========================================================
# 5. PORTADA PRINCIPAL  (texto a la izquierda, imagen a la derecha)
# =========================================================

hero_image = find_image("hero")

with st.container(key="home_hero"):

    if hero_image:
        text_col, image_col = st.columns(
            [1.25, 1], gap="large", vertical_alignment="center"
        )
    else:
        text_col, image_col = st.container(), None

    with text_col:
        st.caption("CENTRO DE INVESTIGACIÓN EPIDEMIOLÓGICA")
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

        if st.button("Comenzar investigación", key="start_investigation"):
            st.switch_page("pages/3_Pacientes.py")

    if image_col is not None:
        with image_col:
            st.image(hero_image, use_container_width=True)


# =========================================================
# 6. RESUMEN DE INVESTIGACIÓN
# =========================================================

st.markdown('<div class="home-section-label">SEGUIMIENTO</div>', unsafe_allow_html=True)
st.subheader("Resumen de investigación")
st.markdown(
    '<div class="home-section-description">'
    'Consulta el estado actual de tu actividad en la plataforma.'
    '</div>',
    unsafe_allow_html=True
)

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.metric("Expedientes resueltos", f"{completed}/{total_cases}")

with c2:
    st.metric("Puntuación acumulada", score)

with c3:
    st.metric("Progreso general", f"{progress:.0f}%")

with c4:
    status = (
        "Finalizada"
        if total_cases > 0 and completed >= total_cases
        else "En curso"
    )
    st.metric("Estado", status)

st.progress(progress / 100)


# =========================================================
# 7. INVESTIGACIÓN ACTUAL
# =========================================================

st.markdown('<div class="home-section-label">EXPEDIENTES</div>', unsafe_allow_html=True)
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
    case_title = active_case.get("titulo", "Expediente clínico activo")

    with st.container(key="active_case_panel"):
        st.caption("EXPEDIENTE ACTIVO")
        st.markdown(f"**{case_title}**")
        st.write(
            "Continúa revisando los antecedentes, los hallazgos "
            "clínicos y las pruebas diagnósticas de este expediente."
        )
        if st.button("Continuar con el expediente", key="continue_active_case"):
            st.switch_page("pages/3_Pacientes.py")

else:
    st.write(
        "Todavía no tienes un expediente activo. "
        "Puedes comenzar revisando los casos clínicos disponibles."
    )
    if st.button("Consultar expedientes clínicos", key="open_patient_files"):
        st.switch_page("pages/3_Pacientes.py")


# =========================================================
# 8. ÁREAS DE INVESTIGACIÓN  (tarjetas de color por módulo)
#    Cuadrícula de 3 columnas: 7 módulos = 3 + 3 + 1
# =========================================================

st.markdown('<div class="home-section-label">PLATAFORMA</div>', unsafe_allow_html=True)
st.subheader("Áreas de investigación")
st.markdown(
    '<div class="home-section-description">'
    'Accede a las diferentes herramientas de análisis y aprendizaje.'
    '</div>',
    unsafe_allow_html=True
)

COLUMNS_PER_ROW = 3

for start in range(0, len(modules), COLUMNS_PER_ROW):

    columns = st.columns(COLUMNS_PER_ROW, gap="medium")

    for col, module in zip(columns, modules[start:start + COLUMNS_PER_ROW]):

        number, title, description, path, image_name = module
        card_image = find_image(image_name)
        color = MODULE_COLORS.get(number, "#0B7A6E")

        with col:
            with st.container(key=f"card_{number}"):

                if card_image:
                    st.image(card_image, use_container_width=True)
                else:
                    st.markdown(
                        f'<div class="card-icon-band" '
                        f'style="background: linear-gradient(120deg, '
                        f'#12394A 0%, {color} 170%);">'
                        f'{icon_svg(number)}'
                        f'<span class="band-number">{number}</span></div>',
                        unsafe_allow_html=True
                    )

                st.markdown(
                    f'<div class="card-body">'
                    f'<div class="module-number" style="color:{color}">ÁREA {number}</div>'
                    f'<div class="module-title">{title}</div>'
                    f'<div class="module-description">{description}</div>'
                    f'</div>',
                    unsafe_allow_html=True
                )

                if st.button(
                    "Ingresar al módulo",
                    key=f"open_module_{number}",
                    use_container_width=True
                ):
                    st.switch_page(path)

    st.write("")


# =========================================================
# 9. METODOLOGÍA
# =========================================================

st.markdown('<div class="home-section-label">METODOLOGÍA</div>', unsafe_allow_html=True)
st.subheader("Etapas de la investigación")
st.markdown(
    '<div class="home-section-description">'
    'Conoce el procedimiento que debes seguir durante cada caso clínico.'
    '</div>',
    unsafe_allow_html=True
)

steps = [
    ("1", "Revisión del expediente",
     "Estudia los datos del paciente, sus antecedentes y el motivo de consulta."),
    ("2", "Análisis clínico y epidemiológico",
     "Identifica síntomas, signos de alarma y factores de exposición."),
    ("3", "Selección de pruebas",
     "Solicita las pruebas de laboratorio pertinentes para el escenario."),
    ("4", "Interpretación de resultados",
     "Compara los hallazgos con las características de las enfermedades."),
    ("5", "Diagnóstico diferencial",
     "Selecciona una respuesta y revisa la retroalimentación del caso."),
]

with st.expander("Consultar las etapas de la investigación", expanded=False):
    for num, title, description in steps:
        st.markdown(
            f'<div class="step-item">'
            f'<div class="step-num">{num}</div>'
            f'<div><div class="step-title">{title}</div>'
            f'<div class="step-desc">{description}</div></div>'
            f'</div>',
            unsafe_allow_html=True
        )


# =========================================================
# 10. PIE DE PÁGINA
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