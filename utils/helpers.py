
from pathlib import Path


# =========================================================
# RUTAS DEL PROYECTO
# =========================================================

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
IMAGES_DIR = BASE_DIR / "images"
ASSETS_DIR = BASE_DIR / "assets"


# =========================================================
# FORMATO DE INFORMACIÓN
# =========================================================

def format_information(value):
    """
    Convierte información de diferentes tipos
    en un texto legible.
    """

    if value is None:
        return "Información no disponible."

    if isinstance(value, str):
        return value.strip() or "Información no disponible."

    if isinstance(value, (list, tuple, set)):

        items = [
            str(item).strip()
            for item in value
            if item is not None and str(item).strip()
        ]

        if not items:
            return "Información no disponible."

        return "\n".join(f"- {item}" for item in items)

    if isinstance(value, dict):

        if not value:
            return "Información no disponible."

        lines = []

        for key, item in value.items():
            lines.append(
                f"- **{str(key).replace('_', ' ').title()}:** "
                f"{format_information(item)}"
            )

        return "\n".join(lines)

    return str(value)


# =========================================================
# NORMALIZACIÓN DE TEXTO
# =========================================================

def normalize_text(value):
    """
    Normaliza un texto para facilitar comparaciones
    sin distinguir mayúsculas, espacios o tildes.
    """

    import unicodedata

    if value is None:
        return ""

    text = str(value).strip().lower()

    normalized = unicodedata.normalize("NFD", text)

    return "".join(
        character
        for character in normalized
        if unicodedata.category(character) != "Mn"
    )


# =========================================================
# VALIDACIÓN DE DATOS
# =========================================================

def safe_list(value):
    """Devuelve una lista válida a partir de un valor."""

    if value is None:
        return []

    if isinstance(value, list):
        return value

    if isinstance(value, (tuple, set)):
        return list(value)

    if isinstance(value, str):
        return [value] if value.strip() else []

    return [value]


def safe_dict(value):
    """Devuelve un diccionario válido."""

    if isinstance(value, dict):
        return value

    return {}


def get_display_name(data, fallback="Información no disponible"):
    """
    Obtiene un nombre legible desde un diccionario.
    """

    if not isinstance(data, dict):
        return fallback

    return (
        data.get("nombre")
        or data.get("titulo")
        or data.get("name")
        or fallback
    )


# =========================================================
# FORMATO DE IDENTIFICADORES
# =========================================================

def format_identifier(value):
    """Convierte un identificador a un formato legible."""

    if not value:
        return ""

    return str(value).replace("_", " ").replace("-", " ").upper()


# =========================================================
# FORMATO DE RESULTADOS
# =========================================================

def get_result_status(result):
    """
    Clasifica un resultado de laboratorio.

    Devuelve:
    positivo, negativo o indeterminado.
    """

    if result is None:
        return "indeterminado"

    text = normalize_text(result)

    if "positivo" in text:
        return "positivo"

    if "negativo" in text:
        return "negativo"

    return "indeterminado"


# =========================================================
# VALIDACIÓN DE ARCHIVOS
# =========================================================

def file_exists(relative_path):
    """
    Comprueba si existe un archivo dentro del proyecto.
    """

    path = BASE_DIR / relative_path

    return path.is_file()


def get_project_path(relative_path):
    """
    Devuelve la ruta absoluta de un archivo del proyecto.
    """

    return BASE_DIR / relative_path
