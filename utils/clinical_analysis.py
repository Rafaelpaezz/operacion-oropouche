
"""
OPERACIÓN OROPOUCHE
Motor de análisis clínico.

Este módulo organiza y analiza los hallazgos de un expediente
para apoyar la investigación académica y el diagnóstico diferencial.

No genera diagnósticos médicos definitivos.
"""

from typing import Any


# =========================================================
# CONSTANTES CLÍNICAS
# =========================================================

SYMPTOM_GROUPS = {
    "sindrome_febril": [
        "fiebre",
        "escalofrios"
    ],
    "manifestaciones_neurologicas": [
        "cefalea",
        "fotofobia",
        "rigidez de nuca",
        "confusion",
        "letargo",
        "irritabilidad"
    ],
    "manifestaciones_musculares": [
        "mialgia",
        "dolor lumbar"
    ],
    "manifestaciones_articulares": [
        "artralgia",
        "rigidez articular"
    ],
    "manifestaciones_cutaneas": [
        "exantema",
        "prurito"
    ],
    "manifestaciones_digestivas": [
        "nauseas",
        "vomitos",
        "diarrea",
        "dolor abdominal"
    ],
    "manifestaciones_oculares": [
        "conjuntivitis",
        "dolor retroocular"
    ],
    "manifestaciones_hemorragicas": [
        "sangrado",
        "sangrado de mucosas"
    ]
}


WARNING_SIGNS = [
    "dolor abdominal intenso",
    "vomitos persistentes",
    "sangrado de mucosas",
    "letargo o irritabilidad",
    "acumulacion de liquidos",
    "dificultad respiratoria",
    "disminucion de la diuresis",
    "hipotension o signos de mala perfusion"
]


DISEASE_CLINICAL_PROFILES = {
    "dengue": {
        "symptoms": [
            "fiebre",
            "cefalea",
            "dolor retroocular",
            "mialgia",
            "artralgia",
            "nauseas",
            "vomitos",
            "exantema"
        ],
        "clues": [
            "sangrado",
            "dolor abdominal",
            "vomitos persistentes"
        ]
    },

    "oropouche": {
        "symptoms": [
            "fiebre",
            "cefalea",
            "mialgia",
            "artralgia",
            "escalofrios",
            "fotofobia",
            "nauseas",
            "vomitos"
        ],
        "clues": [
            "exposicion a jejenes o pequeños dipteros",
            "residencia en zona rural",
            "contacto con zonas selvaticas"
        ]
    },

    "chikungunya": {
        "symptoms": [
            "fiebre",
            "artralgia",
            "rigidez articular",
            "mialgia",
            "exantema"
        ],
        "clues": [
            "dolor articular intenso",
            "persistencia de artralgias"
        ]
    },

    "zika": {
        "symptoms": [
            "exantema",
            "prurito",
            "conjuntivitis",
            "fiebre",
            "artralgia",
            "cefalea"
        ],
        "clues": [
            "conjuntivitis no purulenta",
            "embarazo"
        ]
    },

    "fiebre_amarilla": {
        "symptoms": [
            "fiebre",
            "cefalea",
            "mialgia",
            "nauseas",
            "vomitos"
        ],
        "clues": [
            "ictericia",
            "manifestaciones hemorragicas",
            "exposicion en zona de riesgo",
            "ausencia de vacunacion contra fiebre amarilla"
        ]
    },

    "mayaro": {
        "symptoms": [
            "fiebre",
            "artralgia",
            "mialgia",
            "exantema",
            "cefalea"
        ],
        "clues": [
            "dolor articular persistente",
            "exposicion a zonas selvaticas"
        ]
    },

    "malaria": {
        "symptoms": [
            "fiebre",
            "escalofrios",
            "cefalea",
            "sudoracion",
            "nauseas",
            "vomitos"
        ],
        "clues": [
            "exposicion en zona endemica",
            "episodios febriles recurrentes"
        ]
    },

    "leptospirosis": {
        "symptoms": [
            "fiebre",
            "cefalea",
            "mialgia",
            "dolor lumbar",
            "nauseas",
            "vomitos"
        ],
        "clues": [
            "exposicion a aguas potencialmente contaminadas",
            "sufusion conjuntival",
            "ictericia"
        ]
    }
}


# =========================================================
# NORMALIZACIÓN DE DATOS
# =========================================================

def normalize_text(value: Any) -> str:
    """Normaliza texto para comparar hallazgos."""

    import unicodedata

    if value is None:
        return ""

    text = str(value).strip().lower()

    text = unicodedata.normalize("NFD", text)

    text = "".join(
        char for char in text
        if unicodedata.category(char) != "Mn"
    )

    return text


def normalize_list(values: Any) -> list[str]:
    """Convierte diferentes estructuras en listas normalizadas."""

    if values is None:
        return []

    if isinstance(values, str):
        values = [values]

    if not isinstance(values, (list, tuple, set)):
        return []

    return [
        normalize_text(value)
        for value in values
        if normalize_text(value)
    ]


def get_patient_data(patient: dict) -> dict:
    """Obtiene los campos clínicos del expediente."""

    if not isinstance(patient, dict):
        raise ValueError(
            "El expediente debe ser un diccionario válido."
        )

    return {
        "nombre": patient.get("nombre", "Paciente sin identificar"),
        "edad": patient.get("edad"),
        "sexo": patient.get("sexo", "No especificado"),
        "dia_evolucion": patient.get(
            "dia_evolucion",
            patient.get("dias_evolucion")
        ),
        "motivo_consulta": patient.get("motivo_consulta", ""),
        "sintomas": normalize_list(patient.get("sintomas")),
        "antecedentes": normalize_list(patient.get("antecedentes")),
        "exposicion": normalize_list(patient.get("exposicion")),
        "signos_vitales": patient.get("signos_vitales", {}),
        "signos_alarma": normalize_list(
            patient.get("signos_alarma")
        ),
        "observaciones": patient.get("observaciones", "")
    }


# =========================================================
# ANÁLISIS DE SÍNTOMAS
# =========================================================

def analyze_symptoms(patient: dict) -> dict:
    """Agrupa los síntomas presentes por sistema o manifestación."""

    data = get_patient_data(patient)

    symptoms = data["sintomas"]

    grouped = {}

    for group_name, group_symptoms in SYMPTOM_GROUPS.items():

        matches = [
            symptom
            for symptom in group_symptoms
            if normalize_text(symptom) in symptoms
        ]

        if matches:
            grouped[group_name] = matches

    return {
        "total_sintomas": len(symptoms),
        "sintomas_registrados": symptoms,
        "grupos_clinicos": grouped,
        "grupos_identificados": list(grouped.keys())
    }


# =========================================================
# ANÁLISIS DE ANTECEDENTES
# =========================================================

def analyze_history(patient: dict) -> dict:
    """Identifica antecedentes relevantes."""

    data = get_patient_data(patient)

    history = data["antecedentes"]

    relevant = {
        "embarazo": [],
        "enfermedades_cronicas": [],
        "inmunosupresion": [],
        "antecedentes_arbovirus": [],
        "vacunacion": [],
        "viajes": [],
        "otros": []
    }

    for item in history:

        if "embarazo" in item:
            relevant["embarazo"].append(item)

        elif "cronicas" in item:
            relevant["enfermedades_cronicas"].append(item)

        elif "inmunosupresion" in item:
            relevant["inmunosupresion"].append(item)

        elif "arbovirus" in item or "dengue" in item:
            relevant["antecedentes_arbovirus"].append(item)

        elif "vacunacion" in item or "vacuna" in item:
            relevant["vacunacion"].append(item)

        elif "viajes" in item or "viaje" in item:
            relevant["viajes"].append(item)

        else:
            relevant["otros"].append(item)

    return {
        "antecedentes_registrados": history,
        "antecedentes_relevantes": relevant
    }


# =========================================================
# ANÁLISIS EPIDEMIOLÓGICO
# =========================================================

def analyze_exposure(patient: dict) -> dict:
    """Clasifica los factores de exposición epidemiológica."""

    data = get_patient_data(patient)

    exposure = data["exposicion"]

    categories = {
        "exposicion_vectorial": [],
        "exposicion_geografica": [],
        "exposicion_ambiental": [],
        "otros_factores": []
    }

    for item in exposure:

        if any(term in item for term in [
            "mosquito",
            "jejen",
            "diptero",
            "vector"
        ]):
            categories["exposicion_vectorial"].append(item)

        elif any(term in item for term in [
            "rural",
            "urbana",
            "viaje",
            "selvatica",
            "municipio",
            "departamento"
        ]):
            categories["exposicion_geografica"].append(item)

        elif any(term in item for term in [
            "agua",
            "agricola",
            "contaminada"
        ]):
            categories["exposicion_ambiental"].append(item)

        else:
            categories["otros_factores"].append(item)

    return {
        "factores_registrados": exposure,
        "categorias": categories
    }


# =========================================================
# ANÁLISIS DE SIGNOS VITALES
# =========================================================

def analyze_vital_signs(patient: dict) -> dict:
    """Organiza signos vitales y señala valores para revisión."""

    data = get_patient_data(patient)

    vital_signs = data["signos_vitales"]

    if not isinstance(vital_signs, dict):
        vital_signs = {}

    findings = []

    temperature = vital_signs.get("temperatura")

    if isinstance(temperature, (int, float)):
        if temperature >= 38:
            findings.append(
                "Temperatura elevada compatible con fiebre."
            )

    heart_rate = vital_signs.get("frecuencia_cardiaca")

    if isinstance(heart_rate, (int, float)):
        if heart_rate > 100:
            findings.append(
                "Frecuencia cardíaca elevada; requiere interpretación "
                "según edad, contexto y estado clínico."
            )

    respiratory_rate = vital_signs.get("frecuencia_respiratoria")

    if isinstance(respiratory_rate, (int, float)):
        if respiratory_rate > 20:
            findings.append(
                "Frecuencia respiratoria elevada; requiere valoración "
                "según edad y contexto."
            )

    oxygen = vital_signs.get("saturacion_oxigeno")

    if isinstance(oxygen, (int, float)):
        if oxygen < 94:
            findings.append(
                "Saturación de oxígeno inferior al 94 %; requiere "
                "valoración clínica."
            )

    pressure = vital_signs.get("presion_arterial")

    if pressure:
        findings.append(
            "Presión arterial registrada: "
            f"{pressure}. Interpretar según edad, contexto y perfusión."
        )

    return {
        "signos_registrados": vital_signs,
        "hallazgos": findings
    }


# =========================================================
# IDENTIFICACIÓN DE SIGNOS DE ALARMA
# =========================================================

def analyze_warning_signs(patient: dict) -> dict:
    """Identifica hallazgos de alarma registrados en el expediente."""

    data = get_patient_data(patient)

    recorded_signs = data["signos_alarma"]

    detected = [
        sign
        for sign in recorded_signs
        if sign in WARNING_SIGNS
    ]

    return {
        "total_signos": len(detected),
        "signos_identificados": detected,
        "requiere_atencion_prioritaria": bool(detected),
        "mensaje": (
            "Se registran hallazgos que requieren valoración clínica "
            "prioritaria."
            if detected
            else "No se registraron signos de alarma en el expediente."
        )
    }


# =========================================================
# COMPARACIÓN CLÍNICA PRELIMINAR
# =========================================================

def generate_differential_candidates(patient: dict) -> list[dict]:
    """
    Genera candidatos preliminares mediante coincidencias clínicas.

    No representa un diagnóstico ni una probabilidad clínica.
    """

    data = get_patient_data(patient)

    patient_symptoms = set(data["sintomas"])
    patient_exposure = set(data["exposicion"])

    candidates = []

    for disease_id, profile in DISEASE_CLINICAL_PROFILES.items():

        expected_symptoms = {
            normalize_text(item)
            for item in profile["symptoms"]
        }

        expected_clues = {
            normalize_text(item)
            for item in profile["clues"]
        }

        symptom_matches = sorted(
            patient_symptoms.intersection(expected_symptoms)
        )

        exposure_matches = sorted(
            patient_exposure.intersection(expected_clues)
        )

        candidates.append({
            "enfermedad": disease_id,
            "coincidencias_sintomas": symptom_matches,
            "coincidencias_exposicion": exposure_matches,
            "total_coincidencias": (
                len(symptom_matches) + len(exposure_matches)
            ),
            "tipo_resultado": "Coincidencia preliminar",
            "advertencia": (
                "No constituye una probabilidad ni confirma "
                "la presencia de la enfermedad."
            )
        })

    candidates.sort(
        key=lambda item: item["total_coincidencias"],
        reverse=True
    )

    return candidates


# =========================================================
# ANÁLISIS CLÍNICO INTEGRAL
# =========================================================

def analyze_patient(patient: dict) -> dict:
    """
    Ejecuta el análisis integral de un expediente.

    Devuelve información estructurada para utilizarla en
    el diagnóstico diferencial y la generación de informes.
    """

    data = get_patient_data(patient)

    symptoms = analyze_symptoms(patient)
    history = analyze_history(patient)
    exposure = analyze_exposure(patient)
    vital_signs = analyze_vital_signs(patient)
    warning_signs = analyze_warning_signs(patient)

    candidates = generate_differential_candidates(patient)

    return {
        "paciente": {
            "nombre": data["nombre"],
            "edad": data["edad"],
            "sexo": data["sexo"],
            "dia_evolucion": data["dia_evolucion"]
        },

        "motivo_consulta": data["motivo_consulta"],

        "analisis_sintomas": symptoms,

        "analisis_antecedentes": history,

        "analisis_epidemiologico": exposure,

        "analisis_signos_vitales": vital_signs,

        "analisis_signos_alarma": warning_signs,

        "diagnosticos_diferenciales_preliminares": candidates,

        "observaciones": data["observaciones"],

        "estado_analisis": "completado",

        "advertencia_academica": (
            "Este análisis es una herramienta educativa de apoyo. "
            "Las coincidencias clínicas no representan probabilidades "
            "diagnósticas ni sustituyen pruebas de laboratorio, "
            "valoración médica o protocolos oficiales."
        )
    }


# =========================================================
# RESUMEN DEL ANÁLISIS
# =========================================================

def generate_clinical_summary(analysis: dict) -> str:
    """Genera un resumen textual del análisis clínico."""

    if not isinstance(analysis, dict):
        return "No hay un análisis clínico válido disponible."

    patient = analysis.get("paciente", {})

    symptoms = analysis.get("analisis_sintomas", {})

    warning = analysis.get("analisis_signos_alarma", {})

    candidates = analysis.get(
        "diagnosticos_diferenciales_preliminares",
        []
    )

    lines = [
        "RESUMEN DEL ANÁLISIS CLÍNICO",
        "",
        f"Paciente: {patient.get('nombre', 'No identificado')}",
        f"Edad: {patient.get('edad', 'No registrada')}",
        f"Sexo: {patient.get('sexo', 'No especificado')}",
        f"Día de evolución: {patient.get('dia_evolucion', 'No registrado')}",
        "",
        "SÍNTOMAS REGISTRADOS",
        f"Total: {symptoms.get('total_sintomas', 0)}",
        ""
    ]

    for group, items in symptoms.get(
        "grupos_clinicos", {}
    ).items():
        lines.append(
            f"{group.replace('_', ' ').capitalize()}: "
            f"{', '.join(items)}"
        )

    lines.extend([
        "",
        "SIGNOS DE ALARMA",
        warning.get("mensaje", "Sin información"),
        "",
        "CANDIDATOS DIFERENCIALES PRELIMINARES"
    ])

    for candidate in candidates[:3]:
        lines.append(
            f"- {candidate['enfermedad'].replace('_', ' ').capitalize()}: "
            f"{candidate['total_coincidencias']} coincidencias."
        )

    lines.extend([
        "",
        analysis.get("advertencia_academica", "")
    ])

    return "\n".join(lines)
