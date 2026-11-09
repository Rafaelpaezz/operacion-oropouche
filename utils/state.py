
import json
import uuid
from pathlib import Path
from datetime import datetime

import streamlit as st


# =========================================================
# RUTAS DEL PROYECTO
# =========================================================

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"


# =========================================================
# CARGA DE INFORMACIÓN
# =========================================================

def load_json(filename):
    """Carga y valida un archivo JSON."""

    file_path = DATA_DIR / filename

    if not file_path.exists():
        raise FileNotFoundError(
            f"No se encontró el archivo requerido: {file_path}"
        )

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return json.load(file)

    except json.JSONDecodeError as error:
        raise ValueError(
            f"El archivo {filename} contiene un error JSON: {error}"
        ) from error


def load_cases():
    """Carga los casos clínicos preparados."""

    data = load_json("casos_clinicos.json")

    if not isinstance(data, dict):
        raise ValueError(
            "casos_clinicos.json debe contener un objeto JSON."
        )

    return data


def load_diseases():
    """Carga la biblioteca de enfermedades."""

    data = load_json("enfermedades.json")

    if not isinstance(data, dict):
        raise ValueError(
            "enfermedades.json debe contener un objeto JSON."
        )

    return data


# =========================================================
# UTILIDADES INTERNAS
# =========================================================

def _now():
    """Fecha y hora local en formato ISO."""

    return datetime.now().isoformat(timespec="seconds")


def _get_active_manual_record():
    """Obtiene el expediente manual activo."""

    patient_id = st.session_state.get("active_patient_id")

    if not patient_id:
        return None

    return st.session_state.patient_records.get(patient_id)


def _sync_active_manual_record():
    """
    Sincroniza los datos de sesión con el expediente manual.

    Mantiene asociados:
    - Pruebas solicitadas.
    - Resultados de laboratorio.
    - Análisis clínico.
    - Análisis epidemiológico.
    - Diagnóstico diferencial.
    """

    if st.session_state.get("active_record_type") != "manual":
        return False

    record = _get_active_manual_record()

    if record is None:
        return False

    # Recuperar estructuras existentes sin sobrescribirlas.
    if not isinstance(record.get("pruebas"), dict):
        record["pruebas"] = {}

    if not isinstance(record.get("resultados_laboratorio"), dict):
        record["resultados_laboratorio"] = {}

    # Sincronizar pruebas solicitadas.
    for test_id in st.session_state.ordered_tests:

        if test_id not in record["pruebas"]:
            record["pruebas"][test_id] = {
                "estado": "Solicitada",
                "fecha_solicitud": _now()
            }

    # Sincronizar resultados.
    record["resultados_laboratorio"].update(
        st.session_state.lab_results
    )

    # Actualizar el estado de cada prueba que tenga resultado.
    for test_id, result in st.session_state.lab_results.items():

        record["pruebas"][test_id] = {
            **record["pruebas"].get(test_id, {}),
            "estado": "Resultado registrado",
            "resultado": dict(result)
        }

    # Sincronizar análisis.
    record["analisis_clinico"] = dict(
        st.session_state.clinical_analysis
    )

    record["analisis_epidemiologico"] = dict(
        st.session_state.epidemiological_analysis
    )

    record["diagnostico_diferencial"] = list(
        st.session_state.differential_results
    )

    record["fecha_actualizacion"] = _now()

    return True


def _restore_active_manual_record(patient):
    """Recupera los datos guardados de un expediente manual."""

    if not isinstance(patient, dict):
        return

    pruebas = patient.get("pruebas", {})
    resultados = patient.get("resultados_laboratorio", {})

    if not isinstance(pruebas, dict):
        pruebas = {}

    if not isinstance(resultados, dict):
        resultados = {}

    st.session_state.ordered_tests = list(pruebas.keys())
    st.session_state.lab_results = dict(resultados)

    st.session_state.clinical_analysis = dict(
        patient.get("analisis_clinico", {})
        if isinstance(patient.get("analisis_clinico"), dict)
        else {}
    )

    st.session_state.epidemiological_analysis = dict(
        patient.get("analisis_epidemiologico", {})
        if isinstance(patient.get("analisis_epidemiologico"), dict)
        else {}
    )

    st.session_state.differential_results = list(
        patient.get("diagnostico_diferencial", [])
        if isinstance(patient.get("diagnostico_diferencial"), list)
        else []
    )


def _reset_active_encounter():
    """Limpia los datos temporales del expediente activo."""

    st.session_state.ordered_tests = []
    st.session_state.lab_results = {}

    st.session_state.diagnosis_choice = None
    st.session_state.diagnosis_submitted = False
    st.session_state.diagnosis_correct = False

    st.session_state.warning_acknowledged = False
    st.session_state.case_feedback = ""

    st.session_state.clinical_analysis = {}
    st.session_state.epidemiological_analysis = {}
    st.session_state.differential_results = []
    st.session_state.report_data = {}


def _remove_temporary_keys():
    """Elimina selecciones y mensajes temporales."""

    prefixes = (
        "note_",
        "lab_selection_",
        "diagnosis_selection_",
        "last_lab_message_",
        "clinical_",
        "patient_form_",
        "test_result_"
    )

    for key in list(st.session_state.keys()):
        if key.startswith(prefixes):
            del st.session_state[key]


# =========================================================
# INICIALIZACIÓN DEL ESTADO
# =========================================================

def initialize_state():
    """
    Inicializa las variables de sesión.

    No elimina información existente ni reinicia el progreso
    cuando se ejecuta desde una página de Streamlit.
    """

    defaults = {
        "user_name": "Investigador",

        # Tipo y selección de expediente.
        "simulation_started": False,
        "active_case_id": None,
        "active_patient_id": None,
        "active_record_type": None,

        # Expedientes manuales.
        "patient_records": {},

        # Laboratorio.
        "ordered_tests": [],
        "lab_results": {},

        # Diagnóstico.
        "diagnosis_choice": None,
        "diagnosis_submitted": False,
        "diagnosis_correct": False,

        # Signos de alarma.
        "warning_acknowledged": False,

        # Puntuación.
        "challenge_score": 0,
        "total_attempts": 0,

        # Progreso de casos preparados.
        "completed_cases": [],
        "completed_steps": [],
        "mission_completed": False,

        # Historial y retroalimentación.
        "case_feedback": "",
        "case_history": {},

        # Motores de análisis.
        "clinical_analysis": {},
        "epidemiological_analysis": {},
        "differential_results": [],
        "report_data": {},

        # Asistente.
        "assistant_messages": []
    }

    for key, value in defaults.items():

        if key not in st.session_state:
            st.session_state[key] = (
                value.copy()
                if isinstance(value, (list, dict))
                else value
            )

    expected_types = {
        "ordered_tests": list,
        "lab_results": dict,
        "completed_cases": list,
        "completed_steps": list,
        "case_history": dict,
        "patient_records": dict,
        "clinical_analysis": dict,
        "epidemiological_analysis": dict,
        "differential_results": list,
        "report_data": dict,
        "assistant_messages": list
    }

    for key, expected_type in expected_types.items():

        if not isinstance(st.session_state.get(key), expected_type):
            st.session_state[key] = expected_type()

    for key in ("challenge_score", "total_attempts"):

        try:
            st.session_state[key] = max(
                0,
                int(st.session_state.get(key, 0))
            )
        except (TypeError, ValueError):
            st.session_state[key] = 0


# =========================================================
# REGISTRO DE PACIENTES MANUALES
# =========================================================

def register_patient(patient_data):
    """
    Registra un paciente nuevo desde el formulario.

    El expediente queda identificado como MANUAL.
    No genera resultados de laboratorio ni diagnósticos
    automáticamente.
    """

    initialize_state()

    if not isinstance(patient_data, dict):
        return False, "Los datos del paciente no son válidos."

    name = str(patient_data.get("nombre", "")).strip()

    if not name:
        return False, "El nombre del paciente es obligatorio."

    try:
        age = int(patient_data.get("edad"))
    except (TypeError, ValueError):
        return False, "La edad debe ser un número entero."

    if age < 0 or age > 120:
        return False, "La edad debe estar entre 0 y 120 años."

    patient_id = f"paciente_{uuid.uuid4().hex[:10]}"

    record = dict(patient_data)

    record.update({
        "id": patient_id,
        "tipo_expediente": "manual",
        "origen": "Registro manual",
        "fecha_registro": _now(),

        "pruebas": {},
        "resultados_laboratorio": {},

        "analisis_clinico": {},
        "analisis_epidemiologico": {},
        "diagnostico_diferencial": [],

        "diagnostico_correcto": None
    })

    st.session_state.patient_records[patient_id] = record

    st.session_state.active_patient_id = patient_id
    st.session_state.active_case_id = None
    st.session_state.active_record_type = "manual"
    st.session_state.simulation_started = True

    _reset_active_encounter()

    return True, patient_id


def update_patient(patient_id, updated_data):
    """Actualiza los datos generales de un paciente manual."""

    initialize_state()

    if patient_id not in st.session_state.patient_records:
        return False, "No se encontró el expediente solicitado."

    if not isinstance(updated_data, dict):
        return False, "Los datos recibidos no son válidos."

    current_record = st.session_state.patient_records[patient_id]

    protected_fields = {
        "id",
        "tipo_expediente",
        "origen",
        "fecha_registro",
        "fecha_actualizacion",
        "diagnostico_correcto",
        "pruebas",
        "resultados_laboratorio",
        "analisis_clinico",
        "analisis_epidemiologico",
        "diagnostico_diferencial"
    }

    for key, value in updated_data.items():

        if key not in protected_fields:
            current_record[key] = value

    current_record["fecha_actualizacion"] = _now()

    return True, "Expediente actualizado correctamente."


def get_patient_records():
    """Devuelve todos los pacientes registrados manualmente."""

    initialize_state()

    return st.session_state.patient_records


def get_patient(patient_id):
    """Busca un paciente manual por su identificador."""

    initialize_state()

    return st.session_state.patient_records.get(patient_id)


def activate_patient(patient_id):
    """Activa un expediente manual previamente registrado."""

    initialize_state()

    patient = get_patient(patient_id)

    if not patient:
        return False

    # Guardar el expediente anterior antes de cambiar.
    _sync_active_manual_record()

    st.session_state.active_patient_id = patient_id
    st.session_state.active_case_id = None
    st.session_state.active_record_type = "manual"
    st.session_state.simulation_started = True

    _reset_active_encounter()
    _restore_active_manual_record(patient)

    return True


# =========================================================
# ADMINISTRACIÓN DE CASOS PREPARADOS
# =========================================================

def start_case(case_id):
    """
    Abre un caso clínico preparado desde el JSON.

    Conserva el progreso general y reinicia los datos
    particulares del expediente activo.
    """

    initialize_state()

    cases = load_cases()

    if case_id not in cases:
        return False

    case = cases[case_id]

    if not isinstance(case, dict):
        return False

    # Guardar el expediente manual anterior antes del cambio.
    _sync_active_manual_record()

    st.session_state.active_case_id = case_id
    st.session_state.active_patient_id = None
    st.session_state.active_record_type = "prepared"
    st.session_state.simulation_started = True

    _reset_active_encounter()

    return True


# =========================================================
# CONSULTA DEL EXPEDIENTE ACTIVO
# =========================================================

def get_active_case():
    """
    Devuelve el expediente activo.

    Puede ser un caso preparado o un paciente manual.
    """

    initialize_state()

    record_type = st.session_state.get("active_record_type")

    if record_type == "manual":

        patient_id = st.session_state.get("active_patient_id")

        if not patient_id:
            return None

        return st.session_state.patient_records.get(patient_id)

    if record_type == "prepared":

        case_id = st.session_state.get("active_case_id")

        if not case_id:
            return None

        return load_cases().get(case_id)

    return None


def get_active_case_id():
    """Devuelve el identificador del expediente activo."""

    initialize_state()

    if st.session_state.get("active_record_type") == "manual":
        return st.session_state.get("active_patient_id")

    return st.session_state.get("active_case_id")


def get_active_record_type():
    """Devuelve 'manual', 'prepared' o None."""

    initialize_state()

    return st.session_state.get("active_record_type")


# =========================================================
# LABORATORIO
# =========================================================

def order_test(test_id, result_data=None, simulated=False):
    """
    Registra la solicitud de una prueba.

    Caso preparado:
        Recupera el resultado configurado en el JSON.

    Paciente manual:
        Registra la solicitud sin inventar resultados.
        Si se proporciona result_data, también registra
        explícitamente ese resultado.
    """

    initialize_state()

    case = get_active_case()

    if not case:
        return False, "No hay un expediente activo."

    test_id = str(test_id).strip()

    if not test_id:
        return False, "Debes seleccionar una prueba."

    if test_id in st.session_state.ordered_tests:
        return False, "Esta prueba ya fue solicitada."

    record_type = get_active_record_type()

    if record_type == "prepared":

        available_tests = case.get("pruebas", {})

        if not isinstance(available_tests, dict):
            return False, "No hay pruebas configuradas."

        if test_id not in available_tests:
            return False, "La prueba no está disponible para este caso."

        test_data = available_tests[test_id]

        if not isinstance(test_data, dict):
            return False, "La configuración de la prueba no es válida."

        result = dict(test_data)
        result["origen_resultado"] = "Simulación académica"
        result["es_simulado"] = True
        result["fecha_registro"] = _now()

        st.session_state.lab_results[test_id] = result

    elif record_type == "manual":

        if result_data is not None:

            if not isinstance(result_data, dict):
                return False, "El resultado debe tener un formato válido."

            result = dict(result_data)
            result["origen_resultado"] = (
                "Simulación académica"
                if simulated
                else "Resultado introducido"
            )
            result["es_simulado"] = bool(simulated)
            result["fecha_registro"] = _now()

            st.session_state.lab_results[test_id] = result

    else:
        return False, "El tipo de expediente no es válido."

    st.session_state.ordered_tests.append(test_id)

    if record_type == "manual":
        _sync_active_manual_record()

    # Puntuación únicamente para casos preparados.
    if record_type == "prepared":
        if len(st.session_state.ordered_tests) <= 4:
            st.session_state.challenge_score += 5

    return True, "Prueba registrada correctamente."


def record_lab_result(test_id, result_data, simulated=False):
    """
    Registra un resultado de laboratorio en un expediente manual.

    simulated=False:
        Resultado introducido por el investigador.

    simulated=True:
        Resultado procedente de un escenario académico.
    """

    initialize_state()

    if get_active_record_type() != "manual":
        return False, (
            "Esta función está destinada a expedientes "
            "de registro manual."
        )

    if not isinstance(result_data, dict):
        return False, "Los datos del resultado no son válidos."

    test_id = str(test_id).strip()

    if not test_id:
        return False, "Debes indicar el nombre o identificador de la prueba."

    result = dict(result_data)

    result["origen_resultado"] = (
        "Simulación académica"
        if simulated
        else "Resultado introducido"
    )
    result["es_simulado"] = bool(simulated)
    result["fecha_registro"] = _now()

    st.session_state.lab_results[test_id] = result

    if test_id not in st.session_state.ordered_tests:
        st.session_state.ordered_tests.append(test_id)

    _sync_active_manual_record()

    return True, "Resultado registrado correctamente."


def get_ordered_tests():
    """Devuelve las pruebas solicitadas."""

    initialize_state()

    return st.session_state.ordered_tests


def get_lab_results():
    """Devuelve los resultados del expediente activo como diccionario."""

    initialize_state()

    return st.session_state.lab_results


# =========================================================
# ANÁLISIS DEL EXPEDIENTE
# =========================================================

def save_analysis_results(
    clinical=None,
    epidemiological=None,
    differential=None
):
    """
    Guarda los resultados de los motores de análisis.

    Los datos se mantienen en sesión y, si el expediente
    es manual, también se guardan en el registro del paciente.
    """

    initialize_state()

    if clinical is not None:

        if not isinstance(clinical, dict):
            return False, "El análisis clínico debe ser un diccionario."

        st.session_state.clinical_analysis = dict(clinical)

    if epidemiological is not None:

        if not isinstance(epidemiological, dict):
            return False, (
                "El análisis epidemiológico debe ser un diccionario."
            )

        st.session_state.epidemiological_analysis = dict(
            epidemiological
        )

    if differential is not None:

        if not isinstance(differential, list):
            return False, (
                "El diagnóstico diferencial debe ser una lista."
            )

        st.session_state.differential_results = list(differential)

    if get_active_record_type() == "manual":
        _sync_active_manual_record()

    return True, "Análisis guardado correctamente."


def get_analysis_results():
    """Devuelve los análisis asociados al expediente activo."""

    initialize_state()

    return {
        "clinico": st.session_state.clinical_analysis,
        "epidemiologico": st.session_state.epidemiological_analysis,
        "diferencial": st.session_state.differential_results
    }


# =========================================================
# SIGNOS DE ALARMA
# =========================================================

def acknowledge_warning_signs():
    """
    Registra el reconocimiento de signos de alarma.

    Otorga puntos únicamente en casos preparados.
    """

    initialize_state()

    case = get_active_case()

    if not case:
        return False

    warning_signs = case.get("signos_alarma", [])

    if not warning_signs:
        return False

    if not st.session_state.warning_acknowledged:

        st.session_state.warning_acknowledged = True

        if get_active_record_type() == "prepared":
            st.session_state.challenge_score += 20

    return True


# =========================================================
# EVALUACIÓN DEL DIAGNÓSTICO
# =========================================================

def submit_diagnosis(diagnosis):
    """
    Evalúa el diagnóstico de un caso preparado.

    Los pacientes manuales no se califican automáticamente
    porque no tienen un diagnóstico correcto predefinido.
    """

    initialize_state()

    case = get_active_case()

    if not case:
        return False, "No hay un expediente activo."

    if get_active_record_type() == "manual":
        return False, (
            "Este expediente fue registrado manualmente. "
            "Su diagnóstico debe construirse mediante el "
            "análisis diferencial, no mediante la calificación "
            "automática de los casos preparados."
        )

    case_id = get_active_case_id()

    if st.session_state.diagnosis_submitted:
        return (
            st.session_state.diagnosis_correct,
            "Este expediente ya fue evaluado."
        )

    if case_id in st.session_state.completed_cases:
        return False, (
            "Este caso ya fue completado. "
            "No es posible volver a obtener puntos por él."
        )

    if not diagnosis:
        return False, "Debes seleccionar un diagnóstico."

    diseases = load_diseases()

    if diagnosis not in diseases:
        return False, "El diagnóstico seleccionado no existe."

    correct_diagnosis = case.get("diagnostico_correcto")

    if not correct_diagnosis:
        return False, "El caso no tiene un diagnóstico configurado."

    if correct_diagnosis not in diseases:
        return False, (
            "El diagnóstico esperado no está configurado "
            "en la biblioteca de enfermedades."
        )

    warning_signs = case.get("signos_alarma", [])

    if warning_signs and not st.session_state.warning_acknowledged:
        return False, (
            "Debes reconocer los signos de alarma antes "
            "de finalizar este desafío."
        )

    st.session_state.diagnosis_choice = diagnosis
    st.session_state.diagnosis_submitted = True
    st.session_state.total_attempts += 1

    is_correct = diagnosis == correct_diagnosis

    st.session_state.diagnosis_correct = is_correct

    explanation = str(
        case.get(
            "explicacion",
            "No hay una explicación adicional configurada."
        )
    )

    if is_correct:

        st.session_state.challenge_score += 100

        st.session_state.case_feedback = (
            "Diagnóstico correcto. " + explanation
        )

    else:

        st.session_state.challenge_score = max(
            0,
            st.session_state.challenge_score - 10
        )

        st.session_state.case_feedback = (
            "El diagnóstico seleccionado no coincide "
            "con el resultado esperado. " + explanation
        )

    st.session_state.completed_cases.append(case_id)

    complete_step(case_id)

    st.session_state.case_history[case_id] = {
        "tipo_expediente": "prepared",
        "diagnostico": diagnosis,
        "diagnostico_correcto": correct_diagnosis,
        "correcto": is_correct,
        "pruebas": list(st.session_state.ordered_tests),
        "resultados": dict(st.session_state.lab_results),
        "signos_alarma_reconocidos": (
            st.session_state.warning_acknowledged
        ),
        "explicacion": explanation,
        "fecha_evaluacion": _now()
    }

    cases = load_cases()

    completed_ids = set(st.session_state.completed_cases)
    valid_ids = set(cases.keys())

    st.session_state.mission_completed = (
        bool(valid_ids)
        and valid_ids.issubset(completed_ids)
    )

    return is_correct, st.session_state.case_feedback


# =========================================================
# PUNTUACIÓN
# =========================================================

def get_score():
    """Devuelve la puntuación acumulada."""

    initialize_state()

    return st.session_state.challenge_score


def get_total_attempts():
    """Devuelve el total de diagnósticos evaluados."""

    initialize_state()

    return st.session_state.total_attempts


# =========================================================
# PROGRESO DE CASOS PREPARADOS
# =========================================================

def get_progress():
    """Calcula el progreso de los casos preparados."""

    initialize_state()

    cases = load_cases()

    if not cases:
        return 0

    valid_ids = set(cases.keys())
    completed = set(st.session_state.completed_cases)

    return len(completed.intersection(valid_ids)) / len(valid_ids)


def get_completed_count():
    """Devuelve el número de casos preparados completados."""

    initialize_state()

    cases = load_cases()

    if not cases:
        return 0

    valid_ids = set(cases.keys())
    completed = set(st.session_state.completed_cases)

    return len(completed.intersection(valid_ids))


def get_total_cases():
    """Devuelve el total de casos preparados."""

    return len(load_cases())


def complete_step(step_name):
    """Registra un paso general sin duplicarlo."""

    initialize_state()

    if step_name not in st.session_state.completed_steps:
        st.session_state.completed_steps.append(step_name)


# =========================================================
# HISTORIAL
# =========================================================

def get_case_history():
    """Devuelve el historial de casos evaluados."""

    initialize_state()

    return st.session_state.case_history


def get_patient_history():
    """Devuelve los expedientes manuales registrados."""

    initialize_state()

    return st.session_state.patient_records


# =========================================================
# REINICIO DE LA SIMULACIÓN
# =========================================================

def reset_simulation():
    """
    Reinicia el progreso de la simulación.

    Conserva el nombre del investigador, pero elimina
    expedientes manuales, resultados e historial de sesión.
    """

    user_name = st.session_state.get(
        "user_name",
        "Investigador"
    )

    keys_to_reset = [
        "simulation_started",
        "active_case_id",
        "active_patient_id",
        "active_record_type",
        "patient_records",

        "ordered_tests",
        "lab_results",

        "diagnosis_choice",
        "diagnosis_submitted",
        "diagnosis_correct",

        "warning_acknowledged",

        "challenge_score",
        "total_attempts",

        "completed_cases",
        "completed_steps",
        "mission_completed",

        "case_feedback",
        "case_history",

        "clinical_analysis",
        "epidemiological_analysis",
        "differential_results",
        "report_data",

        "assistant_messages",
        "confirm_reset"
    ]

    for key in keys_to_reset:

        if key in st.session_state:
            del st.session_state[key]

    _remove_temporary_keys()

    initialize_state()

    st.session_state.user_name = user_name