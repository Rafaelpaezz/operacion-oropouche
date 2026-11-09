
"""
Motor de laboratorio de OPERACIÓN OROPOUCHE.

Responsabilidades:
- Mantener un catálogo académico de pruebas.
- Consultar pruebas por enfermedad.
- Orientar la selección según los días de evolución.
- Interpretar resultados ingresados por el usuario.
- Diferenciar resultados positivos, negativos, indeterminados y pendientes.

IMPORTANTE:
Este módulo es educativo. No reemplaza protocolos oficiales ni
la interpretación de un profesional de laboratorio o de salud.

No genera resultados clínicos automáticamente.
"""

from typing import Any


# ============================================================
# CATÁLOGO DE PRUEBAS
# ============================================================

LABORATORY_TESTS = {
    "oropouche_pcr": {
        "nombre": "RT-PCR para virus Oropouche",
        "metodo": "Molecular",
        "tipo_muestra": "Suero o muestra indicada por el protocolo del laboratorio",
        "enfermedades": ["oropouche"],
        "ventana_orientativa": (1, 7),
        "objetivo": "Detectar material genético del virus.",
        "consideraciones": (
            "La utilidad depende del momento de toma de muestra, "
            "tipo de muestra y protocolo del laboratorio."
        ),
    },
    "dengue_pcr": {
        "nombre": "RT-PCR para dengue",
        "metodo": "Molecular",
        "tipo_muestra": "Suero",
        "enfermedades": ["dengue"],
        "ventana_orientativa": (1, 7),
        "objetivo": "Detectar material genético del virus dengue.",
        "consideraciones": (
            "Es una prueba de detección directa. Su rendimiento depende "
            "del día de evolución y de las condiciones de la muestra."
        ),
    },
    "dengue_ns1": {
        "nombre": "Antígeno NS1 para dengue",
        "metodo": "Antígeno",
        "tipo_muestra": "Suero o plasma, según el ensayo",
        "enfermedades": ["dengue"],
        "ventana_orientativa": (1, 7),
        "objetivo": "Detectar el antígeno NS1 del virus dengue.",
        "consideraciones": (
            "Se utiliza principalmente durante la fase aguda. "
            "Un resultado negativo no descarta por sí solo dengue."
        ),
    },
    "dengue_igm": {
        "nombre": "IgM para dengue",
        "metodo": "Serológico",
        "tipo_muestra": "Suero",
        "enfermedades": ["dengue"],
        "ventana_orientativa": (4, 30),
        "objetivo": "Detectar anticuerpos IgM frente al virus dengue.",
        "consideraciones": (
            "La detección puede ser limitada en los primeros días. "
            "Puede existir reactividad cruzada con otros flavivirus."
        ),
    },
    "chikungunya_pcr": {
        "nombre": "RT-PCR para chikungunya",
        "metodo": "Molecular",
        "tipo_muestra": "Suero",
        "enfermedades": ["chikungunya"],
        "ventana_orientativa": (1, 8),
        "objetivo": "Detectar material genético del virus chikungunya.",
        "consideraciones": (
            "La detección molecular es más útil durante la fase aguda."
        ),
    },
    "chikungunya_igm": {
        "nombre": "IgM para chikungunya",
        "metodo": "Serológico",
        "tipo_muestra": "Suero",
        "enfermedades": ["chikungunya"],
        "ventana_orientativa": (5, 30),
        "objetivo": "Detectar anticuerpos IgM frente al virus chikungunya.",
        "consideraciones": (
            "La serología puede ser negativa al inicio de la enfermedad."
        ),
    },
    "zika_pcr": {
        "nombre": "RT-PCR para virus Zika",
        "metodo": "Molecular",
        "tipo_muestra": "Suero u orina, según el protocolo",
        "enfermedades": ["zika"],
        "ventana_orientativa": (1, 7),
        "objetivo": "Detectar material genético del virus Zika.",
        "consideraciones": (
            "La ventana de detección varía según el tipo de muestra "
            "y el momento de recolección."
        ),
    },
    "zika_igm": {
        "nombre": "IgM para virus Zika",
        "metodo": "Serológico",
        "tipo_muestra": "Suero",
        "enfermedades": ["zika"],
        "ventana_orientativa": (4, 30),
        "objetivo": "Detectar anticuerpos IgM frente al virus Zika.",
        "consideraciones": (
            "Puede presentar reactividad cruzada con otros flavivirus. "
            "La interpretación puede requerir pruebas confirmatorias."
        ),
    },
    "fiebre_amarilla_pcr": {
        "nombre": "RT-PCR para fiebre amarilla",
        "metodo": "Molecular",
        "tipo_muestra": "Muestra definida por el laboratorio de referencia",
        "enfermedades": ["fiebre_amarilla"],
        "ventana_orientativa": (1, 10),
        "objetivo": "Detectar material genético del virus de la fiebre amarilla.",
        "consideraciones": (
            "La selección de muestra y la interpretación deben seguir "
            "las indicaciones del laboratorio de referencia."
        ),
    },
    "fiebre_amarilla_igm": {
        "nombre": "IgM para fiebre amarilla",
        "metodo": "Serológico",
        "tipo_muestra": "Suero",
        "enfermedades": ["fiebre_amarilla"],
        "ventana_orientativa": (5, 30),
        "objetivo": "Detectar anticuerpos IgM frente al virus de la fiebre amarilla.",
        "consideraciones": (
            "Puede existir reactividad cruzada con otros flavivirus. "
            "Requiere interpretación epidemiológica y confirmación cuando corresponda."
        ),
    },
    "mayaro_pcr": {
        "nombre": "RT-PCR para virus Mayaro",
        "metodo": "Molecular",
        "tipo_muestra": "Suero",
        "enfermedades": ["mayaro"],
        "ventana_orientativa": (1, 7),
        "objetivo": "Detectar material genético del virus Mayaro.",
        "consideraciones": (
            "La detección molecular se orienta principalmente a la fase aguda."
        ),
    },
    "mayaro_igm": {
        "nombre": "IgM para virus Mayaro",
        "metodo": "Serológico",
        "tipo_muestra": "Suero",
        "enfermedades": ["mayaro"],
        "ventana_orientativa": (5, 30),
        "objetivo": "Detectar anticuerpos IgM frente al virus Mayaro.",
        "consideraciones": (
            "La interpretación debe considerar posibles reacciones cruzadas "
            "con otros arbovirus."
        ),
    },
    "malaria_gota_gruesa": {
        "nombre": "Gota gruesa y extendido de sangre periférica",
        "metodo": "Microscópico",
        "tipo_muestra": "Sangre periférica",
        "enfermedades": ["malaria"],
        "ventana_orientativa": (1, 30),
        "objetivo": "Identificar parásitos del género Plasmodium.",
        "consideraciones": (
            "La sospecha clínica de malaria requiere evaluación oportuna. "
            "Un resultado negativo puede requerir repetición según el contexto "
            "y el protocolo aplicable."
        ),
    },
    "malaria_prueba_rapida": {
        "nombre": "Prueba rápida para malaria",
        "metodo": "Inmunocromatográfico",
        "tipo_muestra": "Sangre",
        "enfermedades": ["malaria"],
        "ventana_orientativa": (1, 30),
        "objetivo": "Detectar antígenos de Plasmodium.",
        "consideraciones": (
            "Debe interpretarse junto con la evaluación clínica y, "
            "cuando corresponda, la microscopía."
        ),
    },
    "leptospira_pcr": {
        "nombre": "PCR para Leptospira",
        "metodo": "Molecular",
        "tipo_muestra": "Sangre u otra muestra según la fase y el protocolo",
        "enfermedades": ["leptospirosis"],
        "ventana_orientativa": (1, 10),
        "objetivo": "Detectar material genético de Leptospira.",
        "consideraciones": (
            "La muestra apropiada depende de la fase de la enfermedad."
        ),
    },
    "leptospira_igm": {
        "nombre": "IgM para Leptospira",
        "metodo": "Serológico",
        "tipo_muestra": "Suero",
        "enfermedades": ["leptospirosis"],
        "ventana_orientativa": (5, 30),
        "objetivo": "Detectar anticuerpos IgM frente a Leptospira.",
        "consideraciones": (
            "La serología puede ser negativa en etapas tempranas. "
            "La interpretación depende del contexto y del método utilizado."
        ),
    },
}


# ============================================================
# FUNCIONES DE CONSULTA
# ============================================================

def get_all_tests() -> list[dict]:
    """Devuelve todas las pruebas disponibles en el catálogo."""
    return [
        {"id": test_id, **test_data}
        for test_id, test_data in LABORATORY_TESTS.items()
    ]


def get_test(test_id: str) -> dict | None:
    """Obtiene una prueba por su identificador."""
    if not isinstance(test_id, str):
        return None

    test = LABORATORY_TESTS.get(test_id)

    if test is None:
        return None

    return {"id": test_id, **test}


def get_tests_by_disease(disease_id: str) -> list[dict]:
    """Devuelve las pruebas asociadas a una enfermedad."""
    if not isinstance(disease_id, str):
        return []

    disease_id = disease_id.strip().lower()

    return [
        {"id": test_id, **test_data}
        for test_id, test_data in LABORATORY_TESTS.items()
        if disease_id in test_data["enfermedades"]
    ]


def get_recommended_tests(
    disease_id: str,
    days_of_evolution: int | None = None
) -> list[dict]:
    """
    Devuelve pruebas asociadas a una enfermedad.

    Si se proporciona el día de evolución, agrega una orientación
    temporal. No excluye pruebas ni determina por sí sola cuál debe
    solicitarse.
    """
    tests = get_tests_by_disease(disease_id)

    for test in tests:
        start_day, end_day = test["ventana_orientativa"]

        if days_of_evolution is None:
            test["orientacion_temporal"] = (
                "Indique el día de evolución para contextualizar esta prueba."
            )
        elif days_of_evolution < start_day:
            test["orientacion_temporal"] = (
                "La muestra podría encontrarse antes de la ventana "
                "orientativa de detección."
            )
        elif days_of_evolution > end_day:
            test["orientacion_temporal"] = (
                "El paciente podría encontrarse después de la ventana "
                "orientativa indicada."
            )
        else:
            test["orientacion_temporal"] = (
                "El día de evolución se encuentra dentro de la ventana "
                "orientativa indicada."
            )

    return tests


# ============================================================
# VALIDACIÓN DE DATOS
# ============================================================

def validate_test_request(
    test_id: str,
    days_of_evolution: Any
) -> dict:
    """Valida la existencia de una prueba y el día de evolución."""
    test = get_test(test_id)

    if test is None:
        return {
            "valido": False,
            "mensaje": "La prueba seleccionada no existe en el catálogo.",
            "prueba": None,
        }

    try:
        day = int(days_of_evolution)
    except (TypeError, ValueError):
        return {
            "valido": False,
            "mensaje": "El día de evolución debe ser un número entero.",
            "prueba": test,
        }

    if day < 1:
        return {
            "valido": False,
            "mensaje": "El día de evolución debe ser igual o superior a 1.",
            "prueba": test,
        }

    start_day, end_day = test["ventana_orientativa"]

    if day < start_day or day > end_day:
        message = (
            "El día de evolución está fuera de la ventana orientativa "
            "del catálogo. Esto no invalida automáticamente la prueba."
        )
    else:
        message = (
            "El día de evolución está dentro de la ventana orientativa "
            "del catálogo."
        )

    return {
        "valido": True,
        "mensaje": message,
        "prueba": test,
        "dia_evolucion": day,
    }


# ============================================================
# INTERPRETACIÓN DE RESULTADOS
# ============================================================

def normalize_result(value: Any) -> str:
    """Normaliza el resultado ingresado para facilitar su clasificación."""
    if value is None:
        return ""

    return str(value).strip().lower()


def interpret_test_result(
    test_id: str,
    result_data: Any
) -> dict:
    """
    Clasifica un resultado proporcionado por el usuario.

    No interpreta síntomas ni inventa resultados.
    La clasificación no sustituye el informe del laboratorio.
    """
    test = get_test(test_id)

    if test is None:
        return {
            "valido": False,
            "estado": "no_disponible",
            "interpretacion": "No se encontró la prueba en el catálogo.",
        }

    if isinstance(result_data, dict):
        raw_result = (
            result_data.get("resultado")
            or result_data.get("valor")
            or result_data.get("estado")
        )
    else:
        raw_result = result_data

    result = normalize_result(raw_result)

    if not result:
        return {
            "valido": True,
            "estado": "pendiente",
            "interpretacion": "No se ha registrado un resultado.",
            "prueba": test["nombre"],
        }

    positive_values = {
        "positivo", "positiva", "detectado", "detectada",
        "reactivo", "reactiva", "positive", "detected",
    }

    negative_values = {
        "negativo", "negativa", "no detectado", "no detectada",
        "no reactivo", "no reactiva", "negative", "not detected",
    }

    inconclusive_values = {
        "indeterminado", "indeterminada", "inconcluso",
        "inconclusa", "dudoso", "dudosa", "equivoco",
        "equivoca", "inconclusive",
    }

    if result in positive_values:
        status = "positivo"
        interpretation = (
            "El resultado fue registrado como positivo. "
            "Debe correlacionarse con el contexto clínico, epidemiológico, "
            "el método utilizado y las indicaciones del laboratorio."
        )

    elif result in negative_values:
        status = "negativo"
        interpretation = (
            "El resultado fue registrado como negativo. "
            "Un resultado negativo no descarta necesariamente la enfermedad; "
            "deben considerarse el día de evolución, el tipo de muestra "
            "y las características de la prueba."
        )

    elif result in inconclusive_values:
        status = "indeterminado"
        interpretation = (
            "El resultado fue registrado como indeterminado. "
            "Se debe revisar el informe y considerar las indicaciones "
            "del laboratorio para su resolución."
        )

    else:
        status = "no_clasificado"
        interpretation = (
            "Se conservó el resultado original, pero no fue posible "
            "clasificarlo automáticamente. Revise el informe del laboratorio."
        )

    return {
        "valido": True,
        "estado": status,
        "resultado_original": str(raw_result),
        "interpretacion": interpretation,
        "prueba": test["nombre"],
        "metodo": test["metodo"],
        "es_simulado": (
            result_data.get("es_simulado", False)
            if isinstance(result_data, dict)
            else False
        ),
    }


# ============================================================
# RESUMEN DEL ESTUDIO DE LABORATORIO
# ============================================================

def summarize_laboratory_results(
    laboratory_results: Any
) -> dict:
    """
    Resume resultados registrados en un expediente.

    Acepta una lista de diccionarios con campos como:
    test_id, resultado, fecha y es_simulado.
    """
    if not isinstance(laboratory_results, list):
        laboratory_results = []

    summary = {
        "total": len(laboratory_results),
        "positivos": 0,
        "negativos": 0,
        "indeterminados": 0,
        "pendientes": 0,
        "no_clasificados": 0,
        "resultados": [],
    }

    for item in laboratory_results:
        if not isinstance(item, dict):
            continue

        test_id = item.get("test_id") or item.get("id_prueba")
        raw_result = item.get("resultado")

        if not test_id:
            continue

        interpretation = interpret_test_result(test_id, item)

        status = interpretation.get("estado", "no_clasificado")

        if status in summary:
            summary[status + "s" if status != "indeterminado" else "indeterminados"] += 1
        elif status == "pendiente":
            summary["pendientes"] += 1
        else:
            summary["no_clasificados"] += 1

        summary["resultados"].append({
            "test_id": test_id,
            "resultado": raw_result,
            "interpretacion": interpretation,
        })

    return summary
