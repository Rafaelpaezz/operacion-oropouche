
import streamlit as st
from utils.state import initialize_state

initialize_state()

st.set_page_config(
    page_title="OPERACIÓN OROPOUCHE",
    page_icon="🦟",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -----------------------------------------
# ESTILOS GENERALES
# -----------------------------------------

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background: #0b1220;
    color: #edf2f7;
}

[data-testid="stSidebar"] {
    background: #101b2d;
    border-right: 1px solid #24334a;
}

[data-testid="stSidebar"] * {
    color: #e5edf7;
}

#MainMenu, footer, header {
    visibility: hidden;
}

.block-container {
    padding-top: 2.2rem;
    padding-bottom: 3rem;
    max-width: 1450px;
}

.hero {
    background: linear-gradient(115deg, #122d42 0%, #145b62 55%, #167b75 100%);
    border: 1px solid #277d80;
    border-radius: 20px;
    padding: 35px;
    margin-bottom: 25px;
    position: relative;
    overflow: hidden;
}

.hero-label {
    color: #a8e9dc;
    font-size: 12px;
    font-weight: 700;
    letter-spacing: 2px;
    text-transform: uppercase;
}

.hero h1 {
    font-size: 36px;
    line-height: 1.15;
    color: white;
    font-weight: 800;
    margin: 14px 0;
}

.hero p {
    color: #d0e8e8;
    font-size: 15px;
    max-width: 650px;
    line-height: 1.7;
}

.section-title {
    font-size: 21px;
    font-weight: 700;
    color: #f1f5f9;
    margin: 25px 0 15px;
}

.metric-card {
    background: #142237;
    border: 1px solid #263b54;
    border-radius: 15px;
    padding: 19px;
    min-height: 125px;
}

.metric-label {
    color: #9eb0c5;
    font-size: 12px;
    font-weight: 600;
}

.metric-value {
    font-size: 27px;
    font-weight: 800;
    color: #f1f5f9;
    margin-top: 9px;
}

.metric-note {
    font-size: 11px;
    color: #91cfc1;
    margin-top: 5px;
}

.module-card {
    background: #142237;
    border: 1px solid #293d55;
    border-radius: 15px;
    padding: 20px;
    min-height: 180px;
    margin-bottom: 12px;
}

.module-icon {
    font-size: 27px;
    margin-bottom: 12px;
}

.module-card h3 {
    font-size: 16px;
    color: #f1f5f9;
    margin-bottom: 8px;
}

.module-card p {
    color: #9fb1c5;
    font-size: 12px;
    line-height: 1.6;
}

.info-panel {
    background: #142237;
    border: 1px solid #293d55;
    border-radius: 15px;
    padding: 22px;
}

div.stButton > button {
    background: #167d76;
    color: white;
    border: 1px solid #299c90;
    border-radius: 9px;
    font-weight: 600;
    min-height: 42px;
}

div.stButton > button:hover {
    background: #20958a;
    color: white;
    border-color: #52c7b7;
}

hr {
    border-color: #293d55;
}

</style>
""", unsafe_allow_html=True)

# -----------------------------------------
# BARRA LATERAL
# -----------------------------------------

with st.sidebar:
    st.markdown("## 🦟 OROPOUCHE")
    st.caption("PLATAFORMA DE SIMULACIÓN EPIDEMIOLÓGICA")
    st.divider()

    st.markdown("### NAVEGACIÓN")
    st.page_link("app.py", label="Panel principal", icon="🏠")

    st.markdown("### MÓDULOS")
    st.page_link("pages/1_Epidemiologia.py", label="Epidemiología", icon="🌎")
    st.page_link("pages/2_Base_Cientifica.py", label="Base científica", icon="🧬")
    st.page_link("pages/3_Pacientes.py", label="Pacientes", icon="🩺")
    st.page_link("pages/4_Laboratorio.py", label="Laboratorio", icon="🔬")
    st.page_link("pages/5_Asistente_IA.py", label="Asistente IA", icon="🤖")
    st.page_link("pages/6_Desafios.py", label="Desafíos", icon="🎯")
    st.page_link("pages/7_Resultados.py", label="Resultados", icon="📊")

    st.divider()
    st.markdown("**OPERACIÓN OROPOUCHE**")
    st.caption("Simulador educativo de epidemiología y entrenamiento clínico.")
    st.caption("Versión inicial 0.1.0")

# -----------------------------------------
# ENCABEZADO
# -----------------------------------------

st.markdown("""
<div class="hero">
    <div class="hero-label">CENTRO DE OPERACIONES · VIGILANCIA EPIDEMIOLÓGICA</div>
    <h1>OPERACIÓN<br>OROPOUCHE</h1>
    <p>
        Bienvenido al centro de simulación epidemiológica.
        Analiza escenarios, investiga casos clínicos, interpreta
        resultados de laboratorio y toma decisiones basadas
        en evidencia científica frente al virus Oropouche.
    </p>
</div>
""", unsafe_allow_html=True)

# -----------------------------------------
# INDICADORES
# -----------------------------------------

st.markdown('<div class="section-title">Panel de operaciones</div>',
            unsafe_allow_html=True)

c1, c2, c3, c4 = st.columns(4)

metrics = [
    (c1, "ESTADO DEL SIMULADOR", "ACTIVO", "Entorno de entrenamiento"),
    (c2, "MÓDULOS", "07", "Áreas de aprendizaje"),
    (c3, "CASOS CLÍNICOS", "EN PREPARACIÓN", "Escenarios educativos"),
    (c4, "ASISTENTE IA", "PENDIENTE", "Integración programada")
]

for col, label, value, note in metrics:
    with col:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">{label}</div>
            <div class="metric-value">{value}</div>
            <div class="metric-note">{note}</div>
        </div>
        """, unsafe_allow_html=True)

# -----------------------------------------
# MÓDULOS
# -----------------------------------------

st.markdown('<div class="section-title">Áreas de entrenamiento</div>',
            unsafe_allow_html=True)

modules = [
    ("🌎", "Epidemiología", "Explora la distribución, transmisión y comportamiento epidemiológico del virus."),
    ("🧬", "Base científica", "Consulta conceptos, características del virus y fundamentos científicos."),
    ("🩺", "Pacientes", "Analiza historias clínicas y desarrolla escenarios de atención."),
    ("🔬", "Laboratorio", "Interpreta pruebas diagnósticas y resultados de laboratorio."),
    ("🤖", "Asistente IA", "Obtén orientación y apoyo para resolver los escenarios de aprendizaje."),
    ("🎯", "Desafíos", "Resuelve retos clínicos y epidemiológicos mediante toma de decisiones."),
    ("📊", "Resultados", "Consulta tu desempeño y evolución durante la simulación.")
]

for row in range(0, 7, 3):
    cols = st.columns(3)
    for col, item in zip(cols, modules[row:row+3]):
        icon, title, description = item
        with col:
            st.markdown(f"""
            <div class="module-card">
                <div class="module-icon">{icon}</div>
                <h3>{title}</h3>
                <p>{description}</p>
            </div>
            """, unsafe_allow_html=True)

# -----------------------------------------
# INFORMACIÓN INFERIOR
# -----------------------------------------

st.markdown('<div class="section-title">Centro de información</div>',
            unsafe_allow_html=True)

left, right = st.columns([1.5, 1])

with left:
    st.markdown("""
    <div class="info-panel">
        <h3>🦟 Sobre la operación</h3>
        <p style="color:#a9bbce; line-height:1.8; font-size:13px;">
        OPERACIÓN OROPOUCHE es un entorno interactivo de aprendizaje
        diseñado para fortalecer los conocimientos sobre epidemiología,
        diagnóstico y análisis de escenarios relacionados con el virus
        Oropouche.
        </p>
        <p style="color:#91cfc1; font-size:12px;">
        Aprendizaje · Investigación · Análisis · Toma de decisiones
        </p>
    </div>
    """, unsafe_allow_html=True)

with right:
    st.markdown("""
    <div class="info-panel">
        <h3>📌 Estado del proyecto</h3>
        <p style="color:#a9bbce; font-size:13px;">
        Fase 1: Construcción de la plataforma
        </p>
        <p style="color:#91cfc1; font-size:12px;">
        ● Entorno de desarrollo configurado
        </p>
        <p style="color:#91cfc1; font-size:12px;">
        ● Interfaz inicial en construcción
        </p>
        <p style="color:#9eb0c5; font-size:12px;">
        ○ Módulos funcionales pendientes
        </p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")
st.caption(
    "OPERACIÓN OROPOUCHE · Plataforma educativa de simulación. "
    "No sustituye el diagnóstico ni la orientación de profesionales de salud."
)
