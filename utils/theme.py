import streamlit as st


# =========================================================
# PALETA
# Base común para toda la app. Cada módulo tiene su propio
# color de acento (y una versión suave para fondos y etiquetas).
# =========================================================

BASE = {
    "background": "#F4F7F9",
    "surface": "#FFFFFF",
    "primary": "#12394A",
    "text": "#1B2F36",
    "muted": "#4A5F67",
    "border": "#DCE4E8",
}

# (acento, acento suave)
ACCENTS = {
    "inicio":        ("#0B7A6E", "#E0F2EF"),
    "epidemiologia": ("#0B7A6E", "#E0F2EF"),
    "ciencia":       ("#2F5FA7", "#E4ECF8"),
    "pacientes":     ("#B4532A", "#F9EAE2"),
    "laboratorio":   ("#0E7490", "#DFF1F6"),
    "asistente":     ("#6D4BC3", "#ECE7F8"),
    "desafios":      ("#C2410C", "#FDEBDD"),
    "resultados":    ("#15803D", "#E2F3E8"),
}

THEMES = {
    name: {**BASE, "accent": accent, "accent_soft": soft}
    for name, (accent, soft) in ACCENTS.items()
}

# Color de cada módulo por número (se usa en las tarjetas de la portada)
MODULE_COLORS = {
    "01": "#0B7A6E",
    "02": "#2F5FA7",
    "03": "#B4532A",
    "04": "#0E7490",
    "05": "#6D4BC3",
    "06": "#C2410C",
    "07": "#15803D",
}


# =========================================================
# NAVEGACIÓN (barra lateral única para toda la app)
# =========================================================

NAV_ITEMS = [
    ("app.py", "Inicio", ":material/home:"),
    ("pages/1_Epidemiologia.py", "Inteligencia epidemiológica", ":material/public:"),
    ("pages/2_Base_Cientifica.py", "Biblioteca científica", ":material/menu_book:"),
    ("pages/3_Pacientes.py", "Expedientes clínicos", ":material/folder_shared:"),
    ("pages/4_Laboratorio.py", "Laboratorio", ":material/biotech:"),
    ("pages/5_Asistente_IA.py", "Asistente educativo", ":material/smart_toy:"),
    ("pages/6_Desafios.py", "Desafíos médicos", ":material/emoji_events:"),
    ("pages/7_Resultados.py", "Resultados y evaluación", ":material/analytics:"),
]


# =========================================================
# TIPOGRAFÍA (Google Fonts)
# =========================================================

FONTS = """<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Source+Serif+4:wght@600;700&display=swap');
</style>
"""


# =========================================================
# ESTILOS (CSS fijo; los colores vienen de las variables)
# =========================================================

STYLES = """<style>

/* ---------- Fuente ---------- */

html, body, .stApp,
.stApp p, .stApp li, .stApp label, .stApp span,
.stApp button, .stApp input, .stApp textarea,
[data-baseweb="select"], [data-baseweb="tab"] {
    font-family: "Inter", "Segoe UI", Arial, sans-serif;
}

/* No tocar la fuente de los íconos de Streamlit */
[data-testid="stIconMaterial"],
.material-icons,
.material-symbols-rounded {
    font-family: "Material Symbols Rounded" !important;
}

/* ---------- Fondo y layout ---------- */

.stApp,
[data-testid="stAppViewContainer"] {
    background-color: var(--app-background);
    color: var(--app-text);
}

[data-testid="stMain"] {
    background-color: transparent;
}

.block-container {
    max-width: 1250px;
    padding-top: 2.4rem;
    padding-bottom: 3rem;
}

[data-testid="stHeader"] {
    background: transparent;
}

[data-testid="stDecoration"] {
    display: none;
}

footer {
    visibility: hidden;
}

/* Oculta la lista automática de páginas de Streamlit */
[data-testid="stSidebarNav"],
[data-testid="stSidebarNavItems"] {
    display: none !important;
}

/* ---------- Tipografía ---------- */

h1, h2, h3, h4 {
    color: var(--app-primary) !important;
    letter-spacing: -0.3px;
}

h1, h2 {
    font-family: "Source Serif 4", Georgia, "Times New Roman", serif !important;
}

h1 { font-weight: 700 !important; line-height: 1.2 !important; }
h2 { font-weight: 700 !important; }
h3 { font-weight: 650 !important; }

p, li, label, .stMarkdown {
    color: var(--app-text);
}

[data-testid="stMarkdownContainer"] p,
[data-testid="stMarkdownContainer"] li {
    font-size: 1.02rem;
    line-height: 1.7;
}

[data-testid="stCaptionContainer"],
[data-testid="stCaptionContainer"] p {
    color: var(--app-muted);
    font-size: 0.84rem;
}

/* ---------- Banner de cada módulo ---------- */

.st-key-page_hero {
    background: linear-gradient(
        120deg,
        var(--app-primary) 0%,
        var(--app-primary) 42%,
        var(--app-accent) 135%
    );
    border-radius: 14px;
    border-bottom: 4px solid var(--app-accent);
    padding: 30px 36px;
    margin-bottom: 28px;
}

.st-key-page_hero h1 {
    color: #FFFFFF !important;
    font-size: clamp(28px, 3.4vw, 38px) !important;
    margin: 6px 0 10px 0;
}

.st-key-page_hero p {
    color: #E6F0EE !important;
    font-size: 15px;
    line-height: 1.7;
    max-width: 820px;
    margin: 0;
}

.st-key-page_hero [data-testid="stCaptionContainer"] p {
    color: rgba(255,255,255,0.78) !important;
    font-size: 12px;
    font-weight: 700;
    letter-spacing: 1.8px;
}

/* ---------- Barra lateral ---------- */

[data-testid="stSidebar"] {
    background-color: var(--app-surface);
    border-right: 1px solid var(--app-border);
}

[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p {
    color: var(--app-text);
    font-size: 0.95rem;
}

.sidebar-brand {
    padding: 8px 0 16px 0;
    border-bottom: 1px solid var(--app-border);
    margin-bottom: 14px;
}

.sidebar-brand-title {
    color: var(--app-primary);
    font-size: 17px;
    font-weight: 800;
    letter-spacing: 0.3px;
}

.sidebar-brand-subtitle {
    color: var(--app-muted);
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 1.4px;
    margin-top: 5px;
}

/* Enlaces de navegación */
[data-testid="stPageLink"] a {
    border-radius: 8px;
    font-weight: 600;
    text-decoration: none;
}

[data-testid="stPageLink"] a p {
    color: inherit !important;
    margin: 0;
    font-size: 0.95rem;
}

[data-testid="stSidebar"] [data-testid="stPageLink"] a {
    padding: 8px 12px;
    color: #25414A;
}

[data-testid="stSidebar"] [data-testid="stPageLink"] a:hover {
    background-color: var(--app-accent-soft);
    color: var(--app-accent);
}

/* Página actual resaltada */
[data-testid="stSidebar"] [data-testid="stPageLink"] a[aria-current="page"] {
    background-color: var(--app-accent-soft);
    color: var(--app-accent);
    font-weight: 700;
}

/* ---------- Botones ---------- */

.stButton > button,
.stDownloadButton > button,
.stFormSubmitButton > button {
    background-color: var(--app-primary);
    color: #FFFFFF;
    border: 1px solid var(--app-primary);
    border-radius: 8px;
    min-height: 42px;
    padding: 8px 18px;
    font-weight: 650;
    transition: background-color 0.15s ease, border-color 0.15s ease;
}

/* El texto del botón va dentro de un <p>: que herede el color del botón */
.stButton > button p,
.stButton > button span,
.stButton > button div,
.stDownloadButton > button p,
.stDownloadButton > button span,
.stDownloadButton > button div,
.stFormSubmitButton > button p,
.stFormSubmitButton > button span,
.stFormSubmitButton > button div {
    color: inherit !important;
    font-weight: inherit;
    margin: 0;
}

.stButton > button:hover,
.stDownloadButton > button:hover,
.stFormSubmitButton > button:hover {
    background-color: var(--app-accent);
    border-color: var(--app-accent);
    color: #FFFFFF;
}

.stButton > button:focus,
.stDownloadButton > button:focus,
.stFormSubmitButton > button:focus {
    box-shadow: 0 0 0 3px var(--app-accent-soft);
    outline: none;
}

.stButton > button:disabled,
.stDownloadButton > button:disabled {
    background-color: #C9D3D8;
    border-color: #C9D3D8;
    color: #FFFFFF;
    opacity: 0.8;
}

/* ---------- Campos y selectores ---------- */

.stTextInput input,
.stTextArea textarea,
.stNumberInput input,
.stDateInput input,
.stTimeInput input {
    background-color: #FFFFFF;
    color: var(--app-text);
    border: 1px solid #C5D2D8;
    border-radius: 8px;
}

.stTextInput input:focus,
.stTextArea textarea:focus,
.stNumberInput input:focus {
    border-color: var(--app-accent);
    box-shadow: 0 0 0 2px var(--app-accent-soft);
}

.stTextInput input::placeholder,
.stTextArea textarea::placeholder {
    color: #8497A0;
}

.stSelectbox [data-baseweb="select"] > div,
.stMultiSelect [data-baseweb="select"] > div {
    background-color: #FFFFFF;
    color: var(--app-text);
    border-radius: 8px;
    border-color: #C5D2D8;
}

[data-baseweb="popover"] {
    color: var(--app-text);
}

/* ---------- Pestañas ---------- */

[data-baseweb="tab-list"] {
    gap: 6px;
    border-bottom: 1px solid var(--app-border);
}

[data-baseweb="tab"] {
    color: var(--app-muted);
    font-weight: 600;
}

[data-baseweb="tab"][aria-selected="true"] {
    color: var(--app-accent);
}

[data-baseweb="tab-highlight"] {
    background-color: var(--app-accent);
}

/* ---------- Contenedores y tablas ---------- */

[data-testid="stVerticalBlockBorderWrapper"] {
    background-color: var(--app-surface);
    border-color: var(--app-border);
    border-radius: 12px;
}

[data-testid="stDataFrame"] {
    border: 1px solid var(--app-border);
    border-radius: 8px;
    overflow: hidden;
}

[data-testid="stMetric"] {
    background-color: #FFFFFF;
    border: 1px solid var(--app-border);
    border-left: 4px solid var(--app-accent);
    border-radius: 8px;
    padding: 14px 16px;
}

[data-testid="stMetricLabel"],
[data-testid="stMetricLabel"] p {
    color: var(--app-muted);
}

[data-testid="stMetricValue"] {
    color: var(--app-primary);
    font-weight: 800;
}

/* ---------- Mensajes y elementos interactivos ---------- */

[data-testid="stExpander"] {
    background-color: #FFFFFF;
    border: 1px solid var(--app-border);
    border-radius: 9px;
}

[data-testid="stProgressBar"] > div > div {
    background-color: var(--app-accent);
}

hr {
    border-color: var(--app-border);
}

/* ---------- Colores forzados (se ven bien aunque Streamlit esté en modo oscuro) ---------- */

/* Navegación lateral: texto oscuro legible */
[data-testid="stSidebar"] [data-testid="stPageLink"] a,
[data-testid="stSidebar"] [data-testid="stPageLink"] a *,
[data-testid="stSidebar"] [data-testid="stPageLink"] a p,
[data-testid="stSidebar"] [data-testid="stPageLink"] a span {
    color: #25414A !important;
}

[data-testid="stSidebar"] [data-testid="stPageLink"] a:hover,
[data-testid="stSidebar"] [data-testid="stPageLink"] a:hover * {
    color: var(--app-accent) !important;
}

/* Página actual */
[data-testid="stSidebar"] [data-testid="stPageLink"] a[aria-current="page"],
[data-testid="stSidebar"] [data-testid="stPageLink"] a[aria-current="page"] * {
    color: var(--app-accent) !important;
}

/* Etiquetas de campos, radios y casillas */
[data-testid="stWidgetLabel"] p,
[data-testid="stWidgetLabel"] label,
.stRadio label p,
.stCheckbox label p {
    color: var(--app-text) !important;
}

/* Menús desplegables: fondo blanco, texto oscuro */
[data-baseweb="popover"] [data-baseweb="menu"],
[data-baseweb="popover"] ul {
    background-color: #FFFFFF !important;
}

[data-baseweb="popover"] li,
[data-baseweb="popover"] li * {
    color: var(--app-text) !important;
}

[data-baseweb="popover"] li:hover {
    background-color: var(--app-accent-soft) !important;
}

/* Avisos: fondo claro y texto oscuro, un color por tipo.
   El fondo se aplica a TODAS las capas internas del aviso. */

[data-testid="stAlert"] {
    border-radius: 10px !important;
    overflow: hidden;
}

/* Advertencia (amarillo) */
[data-testid="stAlert"]:has([data-testid="stAlertContentWarning"]),
[data-testid="stAlert"]:has([data-testid="stAlertContentWarning"]) div {
    background-color: #FFF6E0 !important;
}
[data-testid="stAlert"]:has([data-testid="stAlertContentWarning"]) {
    border: 1px solid #F2D58A !important;
}
[data-testid="stAlert"]:has([data-testid="stAlertContentWarning"]) * {
    color: #5A4200 !important;
}

/* Información (azul) */
[data-testid="stAlert"]:has([data-testid="stAlertContentInfo"]),
[data-testid="stAlert"]:has([data-testid="stAlertContentInfo"]) div {
    background-color: #E6F1FA !important;
}
[data-testid="stAlert"]:has([data-testid="stAlertContentInfo"]) {
    border: 1px solid #B9D6EE !important;
}
[data-testid="stAlert"]:has([data-testid="stAlertContentInfo"]) * {
    color: #123B5A !important;
}

/* Éxito (verde) */
[data-testid="stAlert"]:has([data-testid="stAlertContentSuccess"]),
[data-testid="stAlert"]:has([data-testid="stAlertContentSuccess"]) div {
    background-color: #E4F4EA !important;
}
[data-testid="stAlert"]:has([data-testid="stAlertContentSuccess"]) {
    border: 1px solid #B5DEC3 !important;
}
[data-testid="stAlert"]:has([data-testid="stAlertContentSuccess"]) * {
    color: #164A2B !important;
}

/* Error (rojo) */
[data-testid="stAlert"]:has([data-testid="stAlertContentError"]),
[data-testid="stAlert"]:has([data-testid="stAlertContentError"]) div {
    background-color: #FDEAEA !important;
}
[data-testid="stAlert"]:has([data-testid="stAlertContentError"]) {
    border: 1px solid #F3BDBD !important;
}
[data-testid="stAlert"]:has([data-testid="stAlertContentError"]) * {
    color: #6B1B1B !important;
}

/* Texto dentro de expanders */
[data-testid="stExpander"] summary,
[data-testid="stExpander"] summary * {
    color: var(--app-primary) !important;
    font-weight: 600;
}

/* ---------- Chat (Asistente educativo) ---------- */

/* Zona inferior fija donde vive la caja de chat */
[data-testid="stBottom"],
[data-testid="stBottom"] > div,
[data-testid="stBottomBlockContainer"] {
    background-color: var(--app-background) !important;
}

/* Caja de escritura */
[data-testid="stChatInput"],
[data-testid="stChatInput"] > div {
    background-color: #FFFFFF !important;
    border-radius: 12px;
}

[data-testid="stChatInput"] {
    border: 1px solid #C5D2D8;
}

[data-testid="stChatInput"]:focus-within {
    border-color: var(--app-accent);
    box-shadow: 0 0 0 2px var(--app-accent-soft);
}

/* El texto que escribes: oscuro y visible */
[data-testid="stChatInput"] textarea {
    background-color: #FFFFFF !important;
    color: var(--app-text) !important;
    -webkit-text-fill-color: var(--app-text) !important;
    caret-color: var(--app-accent);
}

[data-testid="stChatInput"] textarea::placeholder {
    color: #7A8F98 !important;
    -webkit-text-fill-color: #7A8F98 !important;
}

/* Botón de enviar */
[data-testid="stChatInputSubmitButton"] {
    background-color: var(--app-accent) !important;
    border-radius: 8px;
}

[data-testid="stChatInputSubmitButton"] svg {
    fill: #FFFFFF !important;
    color: #FFFFFF !important;
}

/* Mensajes del chat */
[data-testid="stChatMessage"] {
    background-color: #FFFFFF;
    border: 1px solid var(--app-border);
    border-radius: 12px;
    padding: 14px 16px;
}

/* Mensajes del usuario con un tono suave del color del módulo */
[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarUser"]) {
    background-color: var(--app-accent-soft);
    border-color: transparent;
}

[data-testid="stChatMessage"] p,
[data-testid="stChatMessage"] li,
[data-testid="stChatMessage"] span,
[data-testid="stChatMessage"] strong {
    color: var(--app-text) !important;
}

/* Campos de texto normales: asegura que el texto escrito se vea */
.stTextInput input,
.stTextArea textarea,
.stNumberInput input {
    -webkit-text-fill-color: var(--app-text);
}

/* ---------- Responsive ---------- */

@media (max-width: 768px) {
    .block-container {
        padding: 1.2rem 1rem 2rem 1rem;
    }

    .st-key-page_hero {
        padding: 22px 20px;
    }

    h1 { font-size: 30px !important; }
    h2 { font-size: 24px !important; }
}

</style>
"""


# =========================================================
# BARRA LATERAL COMPARTIDA
# =========================================================

def _sidebar_status():
    """Progreso del investigador (si el estado está disponible)."""

    try:
        from utils.state import (
            get_score,
            get_progress,
            get_completed_count,
            get_total_cases,
        )

        completed = get_completed_count()
        total = get_total_cases()
        score = get_score()
        progress = max(0, min(100, get_progress() * 100))

    except Exception:
        return

    st.caption("ESTADO DE INVESTIGACIÓN")
    st.write(f"Expedientes resueltos: {completed} de {total}")
    st.progress(progress / 100)
    st.write(f"Puntuación acumulada: **{score} puntos**")


def render_sidebar():

    with st.sidebar:

        st.markdown("""
<div class="sidebar-brand">
    <div class="sidebar-brand-title">OPERACIÓN OROPOUCHE</div>
    <div class="sidebar-brand-subtitle">INVESTIGACIÓN EN SALUD PÚBLICA</div>
</div>
""", unsafe_allow_html=True)

        st.caption("PERFIL DEL INVESTIGADOR")

        user_name = st.session_state.get("user_name", "Investigador")

        if not user_name or not str(user_name).strip():
            user_name = "Investigador"

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

        st.caption("NAVEGACIÓN")

        for path, label, icon in NAV_ITEMS:
            st.page_link(path, label=label, icon=icon)

        st.divider()

        _sidebar_status()

        st.divider()

        st.caption("Proyecto académico · Colombia")
        st.caption("Casos y resultados simulados.")


# =========================================================
# TEMA GENERAL
# =========================================================

def apply_theme(theme="inicio", sidebar=True):

    colors = THEMES.get(theme, THEMES["inicio"])

    variables = f"""<style>
:root {{
    --app-background: {colors["background"]};
    --app-surface: {colors["surface"]};
    --app-primary: {colors["primary"]};
    --app-accent: {colors["accent"]};
    --app-accent-soft: {colors["accent_soft"]};
    --app-text: {colors["text"]};
    --app-muted: {colors["muted"]};
    --app-border: {colors["border"]};
}}
</style>
"""

    st.markdown(FONTS + variables + STYLES, unsafe_allow_html=True)

    if sidebar:
        render_sidebar()


# =========================================================
# ENCABEZADOS REUTILIZABLES
# =========================================================

def page_header(title, subtitle, eyebrow="OPERACIÓN OROPOUCHE"):

    with st.container(key="page_hero"):

        st.caption(eyebrow)
        st.title(title)

        if subtitle:
            st.write(subtitle)


def section_title(title, description=None):

    st.subheader(title)

    if description:
        st.caption(description)


# =========================================================
# CONTENEDOR INFORMATIVO REUTILIZABLE
# =========================================================

def info_card(title, description, label=None):

    with st.container(border=True):

        if label:
            st.caption(label.upper())

        st.markdown(f"**{title}**")

        if description:
            st.write(description)