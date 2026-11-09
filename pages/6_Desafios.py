
import streamlit as st

from utils.state import (
    initialize_state,
    load_diseases,
    get_active_case,
    get_active_case_id,
    get_active_record_type,
    get_ordered_tests,
    get_lab_results,
    get_analysis_results,
    acknowledge_warning_signs,
    submit_diagnosis,
)

from utils.theme import apply_theme, page_header


# ---------------------------------------------------------
# CONFIGURACIÓN INICIAL
# ---------------------------------------------------------

st.set_page_config(
    page_title="Desafíos diagnósticos | Operación Oropouche",
    page_icon="🎯",
    layout="wide",
)

initialize_state()
apply_theme("desafios")


# ---------------------------------------------------------
# ESTILOS
# ---------------------------------------------------------

st.markdown(
    """
    <style>
    .challenge-intro {
        color: #665B50;
        font-size: 1rem;
        line-height: 1.65;
        max-width: 850px;
        margin-bottom: 1.2rem;
    }

    .challenge-label {
        color: #795333;
        font-size: 0.76rem;
        font-weight: 700;
        letter-spacing: 0.10em;
        text-transform: uppercase;
        margin-bottom: 0.35rem;
    }

    .challenge-muted {
        color: #74695F;
        font-size: 0.88rem;
        line-height: 1.55;
    }

    .challenge-question {
        color: #493D32;
        font-size: 1.12rem;
        font-weight: 650;
        line-height: 1.5;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# ---------------------------------------------------------
# FUNCIONES AUXILIARES
# ---------------------------------------------------------

def safe_text(value, fallback="Información no disponible"):
    """Convierte valores diversos en texto legible."""

    if value is None or value == "":
        return fallback

    if isinstance(value, dict):
        if not value:
            return fallback

        return "\n".join(
            f"**{key.replace('_', ' ').capitalize()}:** {val}"
            for key, val in value.items()
        )

    if isinstance(value, (list, tuple, set)):
        if not value:
            return fallback

        return "\n".join(f"- {item}" for item in value)

    return str(value)


def normalize_results(results):
    """Normaliza resultados de laboratorio en un diccionario."""

    if isinstance(results, dict):
        return results

    if isinstance(results, list):
        normalized = {}

        for index, result in enumerate(results):
            if not isinstance(result, dict):
                continue

            test_id = result.get(
                "test_id",
                result.get("id", f"prueba_{index + 1}")
            )

            normalized[test_id] = result

        return normalized

    return {}


def normalize_tests(tests):
    """Normaliza las pruebas solicitadas."""

    if isinstance(tests, dict):
        return tests

    if isinstance(tests, (list, tuple, set)):
        return list(tests)

    return []


def is_prepared_record(record_type, case):
    """
    Identifica un caso preparado.
    Los expedientes libres nunca deben calificarse
    por comparación con un diagnóstico predeterminado.
    """

    prepared_types = {
        "caso_preparado",
        "prepared",
        "preparado",
    }

    if record_type in prepared_types:
        return True

    return (
        isinstance(case, dict)
        and bool(case.get("diagnostico_correcto"))
    )


def show_analysis_section(title, content):
    """Muestra una sección de análisis si contiene información."""

    if content is None or content == {} or content == []:
        return

    st.markdown(f"#### {title}")

    if isinstance(content, dict):
        for key, value in content.items():
            label = key.replace("_", " ").capitalize()

            st.markdown(f"**{label}**")
            st.write(safe_text(value))

    else:
        st.write(safe_text(content))


def show_laboratory_results(results):
    """Presenta los resultados sin ocultar su origen."""

    if not results:
        st.info(
            "No hay resultados de laboratorio registrados "
            "en este expediente."
        )
        return

    for test_id, result in results.items():

        if not isinstance(result, dict):
            result = {"resultado": result}

        test_name = result.get(
            "nombre",
            result.get("test_name", test_id)
        )

        result_text = result.get(
            "resultado",
            "Sin resultado registrado"
        )

        interpretation = result.get(
            "interpretacion",
            "No se registró una interpretación."
        )

        is_simulated = result.get(
            "es_simulado",
            result.get("simulado", False)
        )

        with st.container(border=True):

            st.markdown(f"**{test_name}**")

            st.write(f"Resultado: {result_text}")

            st.write(
                f"Interpretación: {interpretation}"
            )

            if result.get("fecha"):
                st.caption(
                    f"Fecha de registro: {result['fecha']}"
                )

            if is_simulated:
                st.caption(
                    "Resultado simulado con fines académicos."
                )
            else:
                st.caption(
                    "Resultado registrado en el expediente. "
                    "Verifica su origen y documentación."
                )


# ---------------------------------------------------------
# ENCABEZADO
# ---------------------------------------------------------

page_header(
    "Desafíos diagnósticos",
    "Contrasta la evidencia clínica y epidemiológica para "
    "proponer el diagnóstico más probable en cada expediente.",
    "MÓDULO 06 · TOMA DE DECISIONES",
)

st.markdown(
    """
    <p class="challenge-intro">
        Evalúa los hallazgos del paciente, interpreta las pruebas
        disponibles y construye una decisión diagnóstica
        fundamentada en la información del expediente.
    </p>
    """,
    unsafe_allow_html=True,
)


# ---------------------------------------------------------
# EXPEDIENTE ACTIVO
# ---------------------------------------------------------

case = get_active_case()
active_case_id = get_active_case_id()
record_type = get_active_record_type()

if not isinstance(case, dict) or not case:

    st.warning(
        "No hay un expediente activo para resolver el desafío."
    )

    if st.button(
        "Ir a expedientes clínicos",
        type="primary",
        use_container_width=True,
    ):
        st.switch_page("pages/3_Pacientes.py")

    st.stop()


# ---------------------------------------------------------
# TIPO DE EXPEDIENTE
# ---------------------------------------------------------

prepared_record = is_prepared_record(
    record_type,
    case,
)

if prepared_record:
    st.caption("MODALIDAD · CASO PREPARADO")
else:
    st.caption("MODALIDAD · INVESTIGACIÓN LIBRE")


# ---------------------------------------------------------
# BIBLIOTECA DE ENFERMEDADES
# ---------------------------------------------------------

diseases = load_diseases()

if not isinstance(diseases, dict) or not diseases:

    st.warning(
        "No se pudo cargar la biblioteca de enfermedades. "
        "Verifica data/enfermedades.json."
    )

    st.stop()


# ---------------------------------------------------------
# IDENTIFICACIÓN DEL EXPEDIENTE
# ---------------------------------------------------------

st.markdown(
    f"""
    <div class="challenge-label">
        EXPEDIENTE ACTIVO · {str(active_case_id or 'SIN ID').upper()}
    </div>
    """,
    unsafe_allow_html=True,
)

st.subheader(
    case.get("titulo", case.get("nombre", "Desafío diagnóstico"))
)

st.write(
    "Revisa la evidencia disponible antes de formular "
    "una conclusión."
)


# ---------------------------------------------------------
# CONSULTA DEL ESTADO DEL EXPEDIENTE
# ---------------------------------------------------------

ordered_tests = normalize_tests(
    get_ordered_tests()
)

lab_results = normalize_results(
    get_lab_results()
)

analysis_data = get_analysis_results()

if not isinstance(analysis_data, dict):
    analysis_data = {}


clinical_analysis = analysis_data.get(
    "clinical",
    analysis_data.get("analisis_clinico", {})
)

epidemiological_analysis = analysis_data.get(
    "epidemiological",
    analysis_data.get("analisis_epidemiologico", {})
)

differential_analysis = analysis_data.get(
    "differential",
    analysis_data.get("diagnostico_diferencial", {})
)


# ---------------------------------------------------------
# INDICADORES
# ---------------------------------------------------------

st.divider()

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Día de evolución",
        case.get("dia_evolucion", "N/D"),
    )

with col2:
    st.metric(
        "Pruebas solicitadas",
        len(ordered_tests),
    )

with col3:
    if prepared_record:
        st.metric(
            "Puntuación actual",
            st.session_state.get("challenge_score", 0),
        )
    else:
        st.metric(
            "Modalidad",
            "Caso libre",
        )


# ---------------------------------------------------------
# EVIDENCIA CLÍNICA
# ---------------------------------------------------------

st.divider()

st.markdown("### Evidencia clínica")

st.markdown("**Motivo de consulta**")

st.write(
    case.get(
        "motivo_consulta",
        "No se registró el motivo de consulta.",
    )
)

col_symptoms, col_context = st.columns(2, gap="large")

with col_symptoms:

    st.markdown("#### Manifestaciones clínicas")

    symptoms = case.get("sintomas", [])

    if isinstance(symptoms, list) and symptoms:

        for symptom in symptoms:
            st.markdown(f"- {symptom}")

    elif symptoms:
        st.write(symptoms)

    else:
        st.caption("No hay síntomas registrados.")


with col_context:

    st.markdown("#### Contexto epidemiológico")

    st.write(
        safe_text(
            case.get("exposicion"),
            "No hay información epidemiológica registrada.",
        )
    )


# ---------------------------------------------------------
# ANTECEDENTES Y SIGNOS VITALES
# ---------------------------------------------------------

with st.expander("Consultar antecedentes y signos vitales"):

    col_history, col_vitals = st.columns(2)

    with col_history:

        st.markdown("**Antecedentes**")

        st.write(
            safe_text(
                case.get("antecedentes"),
                "No se registraron antecedentes.",
            )
        )

    with col_vitals:

        st.markdown("**Signos vitales**")

        vital_signs = case.get("signos_vitales", {})

        if isinstance(vital_signs, dict) and vital_signs:

            for key, value in vital_signs.items():

                label = key.replace("_", " ").capitalize()

                st.write(f"**{label}:** {value}")

        else:
            st.caption("No hay signos vitales registrados.")


# ---------------------------------------------------------
# ANÁLISIS CLÍNICO Y EPIDEMIOLÓGICO
# ---------------------------------------------------------

if clinical_analysis or epidemiological_analysis:

    st.divider()

    st.markdown("### Análisis de la investigación")

    show_analysis_section(
        "Análisis clínico",
        clinical_analysis,
    )

    show_analysis_section(
        "Análisis epidemiológico",
        epidemiological_analysis,
    )

    show_analysis_section(
        "Diagnóstico diferencial registrado",
        differential_analysis,
    )


# ---------------------------------------------------------
# EVIDENCIA DE LABORATORIO
# ---------------------------------------------------------

st.divider()

st.markdown("### Evidencia de laboratorio")

if lab_results:

    show_laboratory_results(lab_results)

else:

    st.info(
        "Todavía no hay resultados de laboratorio registrados. "
        "Puedes continuar con la evidencia clínica disponible."
    )

    if st.button(
        "Ir al laboratorio",
        use_container_width=True,
    ):
        st.switch_page("pages/4_Laboratorio.py")


# ---------------------------------------------------------
# SIGNOS DE ALARMA
# ---------------------------------------------------------

warning_signs = case.get("signos_alarma", [])

if isinstance(warning_signs, str):
    warning_signs = [warning_signs]

if warning_signs:

    st.divider()

    st.markdown("### Evaluación de signos de alarma")

    st.error(
        "Este expediente contiene hallazgos que requieren "
        "atención clínica prioritaria."
    )

    for sign in warning_signs:
        st.markdown(f"- **{sign}**")

    warning_acknowledged = st.session_state.get(
        "warning_acknowledged",
        False,
    )

    if not warning_acknowledged:

        st.warning(
            "Antes de continuar, debes reconocer los signos "
            "de alarma identificados en el expediente."
        )

        if st.button(
            "Reconozco los signos de alarma",
            type="primary",
            use_container_width=True,
        ):

            acknowledge_warning_signs()
            st.rerun()

        st.stop()

    else:

        st.success(
            "Los signos de alarma fueron reconocidos "
            "durante la investigación."
        )


# ---------------------------------------------------------
# ANOTACIONES DEL INVESTIGADOR
# ---------------------------------------------------------

note_key = f"note_{active_case_id}"

investigator_note = st.session_state.get(
    note_key,
    "",
)

if investigator_note:

    with st.expander("Consultar anotaciones del investigador"):

        st.write(investigator_note)


# ---------------------------------------------------------
# DECISIÓN DIAGNÓSTICA
# ---------------------------------------------------------

st.divider()

st.markdown("### Decisión diagnóstica")

st.markdown(
    """
    <p class="challenge-question">
        ¿Cuál es el diagnóstico que mejor explica el escenario clínico?
    </p>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <p class="challenge-muted">
        Considera las manifestaciones clínicas, los antecedentes,
        la exposición epidemiológica, el día de evolución y los
        resultados de laboratorio disponibles.
    </p>
    """,
    unsafe_allow_html=True,
)


# ---------------------------------------------------------
# MODALIDAD DE CASO PREPARADO
# ---------------------------------------------------------

if prepared_record:

    diagnosis_submitted = st.session_state.get(
        "diagnosis_submitted",
        False,
    )

    options = list(diseases.keys())

    selected_diagnosis = st.selectbox(
        "Diagnóstico propuesto",
        options=options,
        format_func=lambda key: diseases[key].get("nombre", key),
        index=None,
        placeholder="Selecciona una enfermedad",
        disabled=diagnosis_submitted,
        key=f"diagnosis_selection_{active_case_id}",
    )

    if not diagnosis_submitted:

        if st.button(
            "Confirmar diagnóstico",
            type="primary",
            use_container_width=True,
            disabled=selected_diagnosis is None,
        ):

            if selected_diagnosis is not None:

                submit_diagnosis(selected_diagnosis)
                st.rerun()

    else:

        st.divider()

        diagnosis_correct = st.session_state.get(
            "diagnosis_correct",
            False,
        )

        if diagnosis_correct:

            st.success(
                "Diagnóstico correcto. Has identificado la "
                "enfermedad esperada para este escenario."
            )

        else:

            st.error(
                "El diagnóstico seleccionado no coincide con "
                "el diagnóstico esperado en este escenario."
            )

        st.markdown("### Retroalimentación")

        feedback = st.session_state.get(
            "case_feedback",
            "No hay retroalimentación disponible.",
        )

        st.write(feedback)

        correct_id = case.get("diagnostico_correcto")

        if correct_id in diseases:

            correct_name = diseases[correct_id].get(
                "nombre",
                correct_id,
            )

            st.info(
                f"**Diagnóstico esperado en este escenario:** "
                f"{correct_name}."
            )

        st.markdown("### Aprendizaje del caso")

        explanation = case.get(
            "explicacion",
            "No se registró una explicación para este caso.",
        )

        st.write(explanation)

        st.caption(
            "La evaluación corresponde a un escenario académico "
            "simulado. No representa una confirmación diagnóstica real."
        )


# ---------------------------------------------------------
# MODALIDAD DE INVESTIGACIÓN LIBRE
# ---------------------------------------------------------

else:

    st.info(
        "Este expediente fue creado mediante investigación libre. "
        "No tiene una respuesta correcta predeterminada y, por tanto, "
        "no será calificado automáticamente."
    )

    selected_diagnosis = st.selectbox(
        "Hipótesis diagnóstica del investigador",
        options=list(diseases.keys()),
        format_func=lambda key: diseases[key].get("nombre", key),
        index=None,
        placeholder="Selecciona una hipótesis diagnóstica",
        key=f"manual_diagnosis_{active_case_id}",
    )

    if selected_diagnosis:

        disease = diseases.get(selected_diagnosis, {})

        st.markdown("#### Enfermedad seleccionada")

        st.write(
            disease.get(
                "descripcion",
                "No hay descripción disponible.",
            )
        )

        st.caption(
            "Esta selección es una hipótesis académica. "
            "No se almacena como diagnóstico confirmado ni recibe "
            "una puntuación de acierto."
        )


# ---------------------------------------------------------
# NAVEGACIÓN
# ---------------------------------------------------------

st.divider()

st.markdown("### Continuar investigación")

col_lab, col_patients, col_results = st.columns(3)

with col_lab:

    if st.button(
        "Consultar laboratorio",
        use_container_width=True,
    ):
        st.switch_page("pages/4_Laboratorio.py")


with col_patients:

    if st.button(
        "Volver a expedientes",
        use_container_width=True,
    ):
        st.switch_page("pages/3_Pacientes.py")


with col_results:

    if prepared_record and st.session_state.get(
        "diagnosis_submitted",
        False,
    ):

        if st.button(
            "Consultar resultados",
            type="primary",
            use_container_width=True,
        ):
            st.switch_page("pages/7_Resultados.py")

    else:

        st.button(
            "Resultados no disponibles",
            disabled=True,
            use_container_width=True,
        )


# ---------------------------------------------------------
# NOTA ACADÉMICA
# ---------------------------------------------------------

st.divider()

st.caption(
    "Los casos preparados, sus resultados y las evaluaciones "
    "son simulados con fines educativos. Los expedientes libres "
    "no constituyen diagnósticos médicos. Esta aplicación no "
    "reemplaza la valoración profesional ni los protocolos "
    "oficiales de vigilancia, diagnóstico y atención."
)
