
from utils.state import load_diseases


# =========================================================
# CONSULTA DE ENFERMEDADES
# =========================================================

def get_disease(disease_id):
    """Obtiene la información de una enfermedad por su identificador."""

    if not disease_id:
        return None

    diseases = load_diseases()
    disease = diseases.get(disease_id)

    return disease if isinstance(disease, dict) else None


def get_all_diseases():
    """Devuelve todas las enfermedades registradas."""

    diseases = load_diseases()

    return diseases if isinstance(diseases, dict) else {}


def get_diseases_by_category(category):
    """Filtra las enfermedades por categoría."""

    if not category:
        return {}

    diseases = get_all_diseases()

    return {
        key: disease
        for key, disease in diseases.items()
        if isinstance(disease, dict)
        and disease.get("categoria") == category
    }


def get_disease_names():
    """Devuelve los nombres de las enfermedades para los selectores."""

    diseases = get_all_diseases()
    names = {}

    for disease_id, disease in diseases.items():

        if not isinstance(disease, dict):
            continue

        name = disease.get("nombre", disease_id)

        names[disease_id] = str(name)

    return names


# =========================================================
# INFORMACIÓN DE EXPEDIENTES
# =========================================================

def get_case_available_tests(case):
    """Devuelve las pruebas disponibles para un expediente."""

    if not isinstance(case, dict):
        return {}

    tests = case.get("pruebas", {})

    return tests if isinstance(tests, dict) else {}


def get_case_warning_signs(case):
    """Devuelve los signos de alarma registrados en un expediente."""

    if not isinstance(case, dict):
        return []

    warning_signs = case.get("signos_alarma", [])

    if isinstance(warning_signs, list):
        return warning_signs

    if isinstance(warning_signs, str):
        return [warning_signs] if warning_signs.strip() else []

    return []


# =========================================================
# RESUMEN DEL DIAGNÓSTICO DIFERENCIAL
# =========================================================

def get_differential_summary():
    """
    Construye un resumen de las enfermedades registradas
    para su consulta y comparación educativa.
    """

    diseases = get_all_diseases()
    summary = []

    for disease_id, disease in diseases.items():

        if not isinstance(disease, dict):
            continue

        summary.append({
            "id": disease_id,
            "nombre": disease.get("nombre", disease_id),
            "categoria": disease.get("categoria", "No especificada"),
            "agente": disease.get("agente", "No especificado"),
            "vector": disease.get("vector", "No especificado")
        })

    return summary


# =========================================================
# CONSULTAS DE INFORMACIÓN CLÍNICA
# =========================================================

def get_disease_tests(disease_id):
    """Obtiene las pruebas diagnósticas asociadas a una enfermedad."""

    disease = get_disease(disease_id)

    if not disease:
        return []

    tests = disease.get("pruebas", [])

    if isinstance(tests, list):
        return tests

    if isinstance(tests, dict):
        return list(tests.values())

    return []


def get_disease_manifestations(disease_id):
    """Obtiene las manifestaciones clínicas de una enfermedad."""

    disease = get_disease(disease_id)

    if not disease:
        return []

    manifestations = disease.get("manifestaciones", [])

    if isinstance(manifestations, list):
        return manifestations

    if isinstance(manifestations, str):
        return [manifestations] if manifestations.strip() else []

    return []


def get_disease_clues(disease_id):
    """Obtiene las pistas clínicas y epidemiológicas de una enfermedad."""

    disease = get_disease(disease_id)

    if not disease:
        return []

    clues = disease.get("pistas", [])

    if isinstance(clues, list):
        return clues

    if isinstance(clues, str):
        return [clues] if clues.strip() else []

    return []
