
"""
Generador de informes de OPERACIÓN OROPOUCHE.

Construye informes académicos a partir de expedientes registrados.
Permite generar una versión Markdown y exportarla a PDF.

IMPORTANTE:
Los informes son herramientas educativas. No constituyen diagnósticos
médicos ni sustituyen la valoración de profesionales de salud.
"""

from datetime import datetime
from pathlib import Path
from typing import Any
from xml.sax.saxutils import escape
import re


ACADEMIC_WARNING = (
    "Este documento pertenece a un ejercicio académico de simulación "
    "e investigación. No constituye un diagnóstico médico, no reemplaza "
    "la valoración profesional ni sustituye los protocolos oficiales."
)


# ============================================================
# FUNCIONES AUXILIARES
# ============================================================

def safe_text(value: Any, default: str = "No registrado") -> str:
    """Convierte un valor en texto legible y seguro."""

    if value is None or value == "":
        return default

    if isinstance(value, bool):
        return "Sí" if value else "No"

    if isinstance(value, (list, tuple, set)):
        if not value:
            return default

        return ", ".join(
            safe_text(item, "")
            for item in value
        )

    if isinstance(value, dict):
        if not value:
            return default

        return "; ".join(
            f"{key}: {safe_text(item, '')}"
            for key, item in value.items()
        )

    return str(value)


def get_first(data: dict, *keys: str, default=None):
    """Obtiene el primer campo disponible entre varias alternativas."""

    if not isinstance(data, dict):
        return default

    for key in keys:
        if key in data and data[key] is not None:
            return data[key]

    return default


def format_section(title: str, content: Any) -> str:
    """Construye una sección Markdown."""

    return f"## {title}\n\n{safe_text(content)}\n"


def format_list(items: Any) -> str:
    """Convierte listas en elementos Markdown."""

    if isinstance(items, dict):
        items = [
            f"{key}: {safe_text(value)}"
            for key, value in items.items()
        ]

    if not isinstance(items, (list, tuple, set)):
        if items:
            return f"- {safe_text(items)}"

        return "- No registrado"

    if not items:
        return "- No registrado"

    return "\n".join(
        f"- {safe_text(item)}"
        for item in items
    )


def sanitize_filename(value: str) -> str:
    """Elimina caracteres no apropiados para un nombre de archivo."""

    value = safe_text(value, "informe")
    value = re.sub(r"[^\w\-]", "_", value, flags=re.UNICODE)

    return value.strip("_") or "informe"


def normalize_laboratory_results(results: Any) -> list:
    """
    Normaliza resultados de laboratorio a una lista de diccionarios.

    Admite:
    - Diccionario indexado por identificador de prueba.
    - Lista de resultados.
    - Diccionario individual con los datos de una prueba.

    Compatible con get_lab_results() de utils/state.py.
    """

    if results is None:
        return []

    if isinstance(results, list):
        normalized = []

        for index, item in enumerate(results, start=1):

            if not isinstance(item, dict):
                continue

            test = dict(item)

            test.setdefault(
                "nombre",
                test.get("test_id", f"Prueba {index}")
            )

            normalized.append(test)

        return normalized

    if not isinstance(results, dict):
        return []

    # Detectar si se recibió directamente un único resultado.
    individual_result_keys = {
        "nombre",
        "prueba",
        "resultado",
        "valor",
        "interpretacion",
        "metodo",
        "estado",
        "es_simulado"
    }

    if individual_result_keys.intersection(results.keys()):
        test = dict(results)

        test.setdefault(
            "nombre",
            test.get("test_id", "Prueba de laboratorio")
        )

        return [test]

    # Diccionario de resultados indexados por test_id.
    normalized = []

    for test_id, result in results.items():

        if not isinstance(result, dict):
            result = {"resultado": result}

        test = dict(result)

        test.setdefault("test_id", str(test_id))
        test.setdefault("nombre", str(test_id))

        normalized.append(test)

    return normalized


def _normalize_differential_results(results: Any) -> list:
    """Normaliza el diagnóstico diferencial."""

    if results is None:
        return []

    if isinstance(results, list):
        return [
            item
            for item in results
            if isinstance(item, (dict, str))
        ]

    if isinstance(results, dict):
        return [
            {"nombre": key, "justificacion": value}
            for key, value in results.items()
        ]

    if isinstance(results, str):
        return [results]

    return []


def _is_simulated_record(patient: dict, laboratory: list) -> bool:
    """Determina si el expediente contiene información simulada."""

    if patient.get("es_simulado") is True:
        return True

    if patient.get("tipo_expediente") == "prepared":
        return True

    if patient.get("tipo_registro") == "caso_preparado":
        return True

    if patient.get("origen") == "Caso preparado":
        return True

    return any(
        item.get("es_simulado") is True
        for item in laboratory
        if isinstance(item, dict)
    )


# ============================================================
# CONSTRUCCIÓN DE DATOS DEL INFORME
# ============================================================

def build_report_data(
    patient: dict,
    clinical_analysis: dict | None = None,
    laboratory_results: Any = None,
    differential_results: Any = None,
    diagnosis: dict | str | None = None,
    report_type: str = "Investigación clínica académica",
    epidemiological_analysis: dict | None = None,
    is_simulation: bool | None = None,
) -> dict:
    """
    Organiza la información del expediente para generar un informe.

    Admite resultados de laboratorio como lista o diccionario.

    Si no se proporcionan análisis explícitos, recupera los que
    estén almacenados dentro del expediente.
    """

    if not isinstance(patient, dict):
        raise TypeError(
            "El expediente del paciente debe ser un diccionario."
        )

    # Recuperar análisis almacenados en el expediente.
    if clinical_analysis is None:
        clinical_analysis = patient.get("analisis_clinico", {})

    if epidemiological_analysis is None:
        epidemiological_analysis = patient.get(
            "analisis_epidemiologico",
            {}
        )

    if differential_results is None:
        differential_results = patient.get(
            "diagnostico_diferencial",
            []
        )

    if laboratory_results is None:
        laboratory_results = patient.get(
            "resultados_laboratorio",
            {}
        )

    if clinical_analysis is None or not isinstance(clinical_analysis, dict):
        clinical_analysis = {}

    if (
        epidemiological_analysis is None
        or not isinstance(epidemiological_analysis, dict)
    ):
        epidemiological_analysis = {}

    laboratory_results = normalize_laboratory_results(
        laboratory_results
    )

    differential_results = _normalize_differential_results(
        differential_results
    )

    patient_name = get_first(
        patient,
        "nombre",
        "name",
        "nombre_completo",
        default="Paciente sin identificar",
    )

    patient_id = get_first(
        patient,
        "id",
        "patient_id",
        "identificador",
        default="No asignado",
    )

    report_date = datetime.now().strftime("%Y-%m-%d %H:%M")

    # Detectar simulación automáticamente si no se indica explícitamente.
    if is_simulation is None:
        is_simulation = _is_simulated_record(
            patient,
            laboratory_results
        )

    return {
        "tipo_informe": report_type,
        "fecha_generacion": report_date,
        "advertencia_academica": ACADEMIC_WARNING,

        "paciente": {
            "nombre": safe_text(patient_name),
            "identificador": safe_text(patient_id),
            "edad": safe_text(get_first(patient, "edad")),
            "sexo": safe_text(get_first(patient, "sexo")),
            "dias_evolucion": safe_text(
                get_first(
                    patient,
                    "dias_evolucion",
                    "dia_evolucion",
                    "dias_de_evolucion",
                )
            ),
            "motivo_consulta": safe_text(
                get_first(
                    patient,
                    "motivo_consulta",
                    "motivo",
                    "consulta",
                )
            ),
            "tipo_expediente": safe_text(
                get_first(
                    patient,
                    "tipo_expediente",
                    "tipo_registro",
                    default="No especificado",
                )
            ),
        },

        "antecedentes": {
            "personales": get_first(
                patient,
                "antecedentes",
                "antecedentes_personales",
                default=[],
            ),
            "epidemiologicos": get_first(
                patient,
                "exposicion",
                "antecedentes_epidemiologicos",
                default=[],
            ),
            "lugar_exposicion": get_first(
                patient,
                "lugar_exposicion",
                "ubicacion_exposicion",
                default="No registrado",
            ),
        },

        "evaluacion_clinica": {
            "sintomas": get_first(
                patient,
                "sintomas",
                "manifestaciones",
                default=[],
            ),
            "signos_vitales": get_first(
                patient,
                "signos_vitales",
                "vitales",
                default={},
            ),
            "signos_alarma": get_first(
                patient,
                "signos_alarma",
                "warning_signs",
                default=[],
            ),
            "observaciones": get_first(
                patient,
                "observaciones",
                "notas",
                default="No registrado",
            ),
            "analisis": clinical_analysis,
        },

        "analisis_epidemiologico": epidemiological_analysis,

        "laboratorio": laboratory_results,

        "diagnostico_diferencial": differential_results,

        "diagnostico_propuesto": diagnosis,

        "es_simulacion": bool(is_simulation),
    }


# ============================================================
# GENERACIÓN DEL INFORME EN MARKDOWN
# ============================================================

def generate_report_markdown(report_data: dict) -> str:
    """Genera el informe completo en formato Markdown."""

    if not isinstance(report_data, dict):
        raise TypeError(
            "Los datos del informe deben ser un diccionario."
        )

    patient = report_data.get("paciente", {})
    antecedentes = report_data.get("antecedentes", {})
    clinical = report_data.get("evaluacion_clinica", {})

    if not isinstance(patient, dict):
        patient = {}

    if not isinstance(antecedentes, dict):
        antecedentes = {}

    if not isinstance(clinical, dict):
        clinical = {}

    lines = [
        "# OPERACIÓN OROPOUCHE",
        "",
        "## Informe de investigación clínica",
        "",
        f"**Tipo de informe:** {safe_text(report_data.get('tipo_informe'))}",
        f"**Fecha de generación:** {safe_text(report_data.get('fecha_generacion'))}",
        f"**Identificador:** {safe_text(patient.get('identificador'))}",
        f"**Tipo de expediente:** {safe_text(patient.get('tipo_expediente'))}",
        f"**Información simulada:** {'Sí' if report_data.get('es_simulacion') else 'No identificada como simulada'}",
        "",
        "---",
        "",
        "## 1. Identificación del paciente",
        "",
        f"- **Nombre:** {safe_text(patient.get('nombre'))}",
        f"- **Edad:** {safe_text(patient.get('edad'))}",
        f"- **Sexo:** {safe_text(patient.get('sexo'))}",
        f"- **Días de evolución:** {safe_text(patient.get('dias_evolucion'))}",
        f"- **Motivo de consulta:** {safe_text(patient.get('motivo_consulta'))}",
        "",
        "## 2. Antecedentes y contexto epidemiológico",
        "",
        "### Antecedentes personales",
        "",
        format_list(antecedentes.get("personales")),
        "",
        "### Exposición epidemiológica",
        "",
        format_list(antecedentes.get("epidemiologicos")),
        "",
        f"**Lugar de exposición:** {safe_text(antecedentes.get('lugar_exposicion'))}",
        "",
        "## 3. Evaluación clínica",
        "",
        "### Síntomas y manifestaciones",
        "",
        format_list(clinical.get("sintomas")),
        "",
        "### Signos vitales",
        "",
        safe_text(clinical.get("signos_vitales")),
        "",
        "### Signos de alarma registrados",
        "",
        format_list(clinical.get("signos_alarma")),
        "",
        f"**Observaciones:** {safe_text(clinical.get('observaciones'))}",
        "",
        "## 4. Análisis clínico",
        "",
    ]

    analysis = clinical.get("analisis", {})

    if isinstance(analysis, dict) and analysis:

        for key, value in analysis.items():

            lines.append(f"### {safe_text(key)}")
            lines.append("")
            lines.append(safe_text(value))
            lines.append("")

    else:
        lines.extend([
            "No se ha incorporado un análisis clínico estructurado.",
            "",
        ])

    # Análisis epidemiológico.
    lines.extend([
        "## 5. Análisis epidemiológico",
        "",
    ])

    epidemiological = report_data.get(
        "analisis_epidemiologico",
        {}
    )

    if isinstance(epidemiological, dict) and epidemiological:

        for key, value in epidemiological.items():

            lines.append(f"### {safe_text(key)}")
            lines.append("")
            lines.append(safe_text(value))
            lines.append("")

    else:
        lines.extend([
            "No se ha incorporado un análisis epidemiológico estructurado.",
            "",
        ])

    # Laboratorio.
    lines.extend([
        "## 6. Pruebas de laboratorio",
        "",
    ])

    laboratory = normalize_laboratory_results(
        report_data.get("laboratorio", [])
    )

    if laboratory:

        for index, test in enumerate(laboratory, start=1):

            test_name = get_first(
                test,
                "nombre",
                "prueba",
                "test_name",
                "test_id",
                default=f"Prueba {index}",
            )

            result = get_first(
                test,
                "resultado",
                "valor",
                "estado",
                default="Pendiente",
            )

            method = get_first(
                test,
                "metodo",
                "método",
                "metodologia",
                default="No registrado",
            )

            date = get_first(
                test,
                "fecha",
                "fecha_registro",
                default="No registrada",
            )

            interpretation = get_first(
                test,
                "interpretacion",
                "interpretación",
                default="No registrada",
            )

            origin = get_first(
                test,
                "origen_resultado",
                default="No especificado",
            )

            simulated = test.get("es_simulado")

            simulation_label = (
                "Sí"
                if simulated is True
                else "No"
                if simulated is False
                else "No especificado"
            )

            lines.extend([
                f"### {index}. {safe_text(test_name)}",
                "",
                f"- **Resultado:** {safe_text(result)}",
                f"- **Método:** {safe_text(method)}",
                f"- **Fecha:** {safe_text(date)}",
                f"- **Interpretación:** {safe_text(interpretation)}",
                f"- **Origen:** {safe_text(origin)}",
                f"- **Resultado simulado:** {simulation_label}",
                "",
            ])

    else:
        lines.extend([
            "No se han registrado pruebas de laboratorio.",
            "",
        ])

    # Diagnóstico diferencial.
    lines.extend([
        "## 7. Diagnóstico diferencial",
        "",
    ])

    differential = report_data.get(
        "diagnostico_diferencial",
        []
    )

    if differential:

        for index, candidate in enumerate(differential, start=1):

            if isinstance(candidate, dict):

                name = get_first(
                    candidate,
                    "nombre",
                    "enfermedad",
                    "disease",
                    "id",
                    default=f"Alternativa {index}",
                )

                reason = get_first(
                    candidate,
                    "justificacion",
                    "motivo",
                    "descripcion",
                    "coincidencias",
                    default="Sin justificación registrada",
                )

                lines.extend([
                    f"### {index}. {safe_text(name)}",
                    "",
                    safe_text(reason),
                    "",
                ])

            else:
                lines.extend([
                    f"- {safe_text(candidate)}",
                    "",
                ])

    else:
        lines.extend([
            "No se ha construido un diagnóstico diferencial.",
            "",
        ])

    # Diagnóstico propuesto.
    lines.extend([
        "## 8. Diagnóstico propuesto",
        "",
        safe_text(
            report_data.get("diagnostico_propuesto"),
            "No se ha registrado un diagnóstico propuesto.",
        ),
        "",
        "## 9. Consideraciones finales",
        "",
        "La información presentada debe analizarse en conjunto con "
        "los antecedentes, la evolución clínica, el contexto epidemiológico "
        "y los resultados de laboratorio disponibles.",
        "",
        "---",
        "",
        "## Advertencia de uso",
        "",
        safe_text(
            report_data.get("advertencia_academica"),
            ACADEMIC_WARNING
        ),
        "",
        "**OPERACIÓN OROPOUCHE | Herramienta académica de investigación.**",
    ])

    return "\n".join(lines)


# ============================================================
# CONVERSIÓN DE TEXTO PARA PDF
# ============================================================

def _markdown_inline_to_reportlab(value: str) -> str:
    """Convierte formatos Markdown básicos a etiquetas ReportLab."""

    value = escape(str(value))

    # Negrita.
    value = re.sub(
        r"\*\*(.*?)\*\*",
        r"<b>\1</b>",
        value
    )

    # Cursiva.
    value = re.sub(
        r"(?<!\*)\*([^*]+)\*(?!\*)",
        r"<i>\1</i>",
        value
    )

    return value


# ============================================================
# EXPORTACIÓN A PDF
# ============================================================

def export_report_pdf(
    report_data: dict,
    output_path: str | Path
) -> str:
    """
    Exporta el informe a PDF utilizando ReportLab.

    Requiere instalar:
        pip install reportlab

    Devuelve la ruta del archivo generado.
    """

    try:
        from reportlab.lib import colors
        from reportlab.lib.enums import TA_CENTER
        from reportlab.lib.pagesizes import A4
        from reportlab.lib.styles import (
            getSampleStyleSheet,
            ParagraphStyle,
        )
        from reportlab.lib.units import cm
        from reportlab.platypus import (
            SimpleDocTemplate,
            Paragraph,
            Spacer,
            HRFlowable,
        )

    except ImportError as error:
        raise ImportError(
            "Para exportar informes a PDF instala ReportLab "
            "con: pip install reportlab"
        ) from error

    markdown = generate_report_markdown(report_data)

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    styles = getSampleStyleSheet()

    styles.add(ParagraphStyle(
        name="ReportTitle",
        parent=styles["Title"],
        fontName="Helvetica-Bold",
        fontSize=20,
        leading=25,
        textColor=colors.HexColor("#1B4550"),
        alignment=TA_CENTER,
        spaceAfter=14,
    ))

    styles.add(ParagraphStyle(
        name="ReportSubtitle",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=9,
        leading=13,
        textColor=colors.HexColor("#52666A"),
        alignment=TA_CENTER,
        spaceAfter=10,
    ))

    styles.add(ParagraphStyle(
        name="ReportHeading",
        parent=styles["Heading2"],
        fontName="Helvetica-Bold",
        fontSize=12,
        leading=16,
        textColor=colors.HexColor("#245B58"),
        spaceBefore=12,
        spaceAfter=6,
        keepWithNext=True,
    ))

    styles.add(ParagraphStyle(
        name="ReportBody",
        parent=styles["BodyText"],
        fontName="Helvetica",
        fontSize=9,
        leading=13,
        spaceAfter=5,
    ))

    styles.add(ParagraphStyle(
        name="ReportWarning",
        parent=styles["BodyText"],
        fontName="Helvetica-Bold",
        fontSize=8,
        leading=11,
        textColor=colors.HexColor("#765B43"),
        backColor=colors.HexColor("#F2EFEA"),
        borderPadding=8,
        spaceBefore=8,
        spaceAfter=8,
    ))

    styles.add(ParagraphStyle(
        name="ReportBullet",
        parent=styles["BodyText"],
        fontName="Helvetica",
        fontSize=9,
        leading=13,
        leftIndent=12,
        firstLineIndent=-8,
        spaceAfter=4,
    ))

    document = SimpleDocTemplate(
        str(output_path),
        pagesize=A4,
        rightMargin=2 * cm,
        leftMargin=2 * cm,
        topMargin=1.8 * cm,
        bottomMargin=1.8 * cm,
        title="OPERACIÓN OROPOUCHE - Informe clínico académico",
        author="OPERACIÓN OROPOUCHE",
    )

    story = []

    for line in markdown.splitlines():

        stripped = line.strip()

        if not stripped:
            story.append(Spacer(1, 4))
            continue

        if stripped == "---":

            story.append(HRFlowable(
                width="100%",
                thickness=0.7,
                color=colors.HexColor("#B9C9C3"),
                spaceBefore=5,
                spaceAfter=8,
            ))

            continue

        if stripped.startswith("# "):

            story.append(Paragraph(
                _markdown_inline_to_reportlab(stripped[2:]),
                styles["ReportTitle"],
            ))

        elif stripped.startswith("## "):

            heading = stripped[3:]

            story.append(Paragraph(
                _markdown_inline_to_reportlab(heading),
                styles["ReportHeading"],
            ))

        elif stripped.startswith("### "):

            story.append(Paragraph(
                f"<b>{_markdown_inline_to_reportlab(stripped[4:])}</b>",
                styles["ReportBody"],
            ))

        elif stripped.startswith("- "):

            story.append(Paragraph(
                f"&bull; {_markdown_inline_to_reportlab(stripped[2:])}",
                styles["ReportBullet"],
            ))

        else:

            safe_line = _markdown_inline_to_reportlab(stripped)

            style = (
                styles["ReportWarning"]
                if "no constituye un diagnóstico" in stripped.lower()
                else styles["ReportBody"]
            )

            story.append(Paragraph(safe_line, style))

    document.build(story)

    return str(output_path)


# ============================================================
# GENERACIÓN DEL NOMBRE DEL ARCHIVO
# ============================================================

def generate_report_filename(
    patient: dict,
    extension: str = "pdf"
) -> str:
    """Genera un nombre de archivo basado en el expediente."""

    if not isinstance(patient, dict):
        patient = {}

    name = get_first(
        patient,
        "nombre",
        "name",
        "nombre_completo",
        default="paciente",
    )

    patient_id = get_first(
        patient,
        "id",
        "patient_id",
        default="expediente",
    )

    safe_name = sanitize_filename(str(name))
    safe_id = sanitize_filename(str(patient_id))

    extension = str(extension).lstrip(".").lower()

    if not extension:
        extension = "pdf"

    return f"informe_{safe_name}_{safe_id}.{extension}"
