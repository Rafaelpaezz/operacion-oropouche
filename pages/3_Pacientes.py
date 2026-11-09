
import streamlit as st

from utils.state import (
    initialize_state,
    load_cases,
    start_case,
    get_active_case,
    get_active_case_id,
    get_active_record_type,
    acknowledge_warning_signs,
    register_patient,
    get_patient_records,
    activate_patient,
    update_patient
)

from utils.theme import apply_theme, page_header


# =========================================================
# CONFIGURACIÓN INICIAL
# =========================================================

st.set_page_config(
    page_title="Expedientes clínicos | Operación Oropouche",
    page_icon="🩺",
    layout="wide"
)

initialize_state()
apply_theme("pacientes")


# =========================================================
# ESTILOS
# =========================================================

st.markdown(
    """
    <style>
    .patient-intro {
        color: #53645F;
        font-size: 1rem;
        line-height: 1.65;
        max-width: 900px;
        margin-bottom: 1rem;
    }

    .patient-label {
        color: #765B43;
        font-size: 0.76rem;
        font-weight: 700;
        letter-spacing: 0.10em;
        text-transform: uppercase;
        margin-bottom: 0.35rem;
    }

    .patient-muted {
        color: #66756F;
        font-size: 0.9rem;
        line-height: 1.55;
    }

    .patient-notice {
        background: rgba(255, 255, 255, 0.65);
        border-left: 4px solid #765B43;
        padding: 0.85rem 1rem;
        border-radius: 5px;
        color: #53645F;
        line-height: 1.55;
        margin: 0.7rem 0 1rem 0;
    }

    div[data-testid="stMetric"] {
        background: rgba(255, 255, 255, 0.65);
        border: 1px solid rgba(90, 105, 95, 0.15);
        border-radius: 10px;
        padding: 0.85rem 1rem;
    }

    div[data-testid="stForm"] {
        background: rgba(255, 255, 255, 0.45);
        border: 1px solid rgba(90, 105, 95, 0.15);
        border-radius: 12px;
        padding: 1.2rem;
    }
    </style>
    """,
    unsafe_allow_html=True
)


# =========================================================
# ENCABEZADO
# =========================================================

page_header(
    "Expedientes clínicos",
    "Registra pacientes, consulta escenarios clínicos y analiza "
    "los hallazgos relevantes para orientar la investigación.",
    "MÓDULO 03 · INVESTIGACIÓN DE PACIENTES"
)

st.markdown(
    """
    <p class="patient-intro">
        Este módulo permite trabajar con pacientes registrados manualmente
        o con escenarios clínicos preparados. La información recopilada
        servirá como punto de partida para el análisis clínico,
        epidemiológico y de laboratorio.
    </p>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class="patient-notice">
        <strong>Alcance académico:</strong> utiliza datos ficticios o
        información clínica debidamente anonimizada. No ingreses nombres
        completos, documentos de identidad, teléfonos ni otros datos
        personales identificables de pacientes reales.
    </div>
    """,
    unsafe_allow_html=True
)


# =========================================================
# FUNCIONES AUXILIARES
# =========================================================

def display_value(value):
    """Convierte diferentes estructuras en texto legible."""

    if value is None:
        return "No registrado"

    if isinstance(value, bool):
        return "Sí" if value else "No"

    if isinstance(value, list):
        return (
            ", ".join(str(item) for item in value)
            if value else "No registrado"
        )

    if isinstance(value, dict):
        if not value:
            return "No registrado"

        return "\n".join(
            f"- {str(key).replace('_', ' ').capitalize()}: {item}"
            for key, item in value.items()
        )

    if str(value).strip() == "":
        return "No registrado"

    return str(value)


def display_list(title, items):
    """Muestra una lista de hallazgos."""

    st.markdown(f"### {title}")

    if isinstance(items, list) and items:
        for item in items:
            st.markdown(f"- {item}")

    elif isinstance(items, str) and items.strip():
        st.write(items)

    else:
        st.caption("No hay información registrada.")


def show_patient_record(case, record_id, record_type):
    """Presenta los datos del expediente activo."""

    st.divider()

    st.markdown(
        f"""
        <div class="patient-label">
            EXPEDIENTE ACTIVO · {record_id.upper()}
        </div>
        """,
        unsafe_allow_html=True
    )

    if record_type == "manual":
        st.caption("Origen: registro manual")

        if case.get("fecha_registro"):
            st.caption(
                f"Fecha de registro: {case['fecha_registro']}"
            )

        title = case.get("nombre", "Paciente registrado")

    else:
        st.caption("Origen: caso clínico preparado")
        title = case.get("titulo", "Expediente clínico")

    st.title(title)

    # -----------------------------------------------------
    # INFORMACIÓN GENERAL
    # -----------------------------------------------------

    st.markdown("### Información general")

    col1, col2, col3 = st.columns(3)

    age = case.get("edad", "N/D")
    sex = case.get("sexo", "No registrado")

    evolution = case.get(
        "dia_evolucion",
        case.get("dias_evolucion", "N/D")
    )

    with col1:
        st.metric(
            "Edad",
            f"{age} años" if str(age) != "N/D" else "N/D"
        )

    with col2:
        st.metric("Sexo", sex)

    with col3:
        st.metric(
            "Evolución clínica",
            f"Día {evolution}" if str(evolution) != "N/D" else "N/D"
        )

    # -----------------------------------------------------
    # MOTIVO DE CONSULTA
    # -----------------------------------------------------

    st.markdown("### Motivo de consulta")

    st.write(
        case.get(
            "motivo_consulta",
            "No se ha registrado información sobre el motivo de consulta."
        )
    )

    # -----------------------------------------------------
    # SÍNTOMAS Y SIGNOS VITALES
    # -----------------------------------------------------

    st.divider()

    col_symptoms, col_vitals = st.columns(2, gap="large")

    with col_symptoms:
        symptoms = case.get("sintomas", [])
        display_list("Síntomas y manifestaciones", symptoms)

    with col_vitals:
        st.markdown("### Signos vitales")

        vital_signs = case.get("signos_vitales", {})

        if isinstance(vital_signs, dict) and vital_signs:
            for key, value in vital_signs.items():
                label = str(key).replace("_", " ").capitalize()
                st.write(f"**{label}:** {value}")
        else:
            st.caption("No hay signos vitales registrados.")

    # -----------------------------------------------------
    # ANTECEDENTES Y EXPOSICIÓN
    # -----------------------------------------------------

    st.divider()

    col_history, col_exposure = st.columns(2, gap="large")

    with col_history:
        st.markdown("### Antecedentes")
        st.write(display_value(case.get("antecedentes")))

    with col_exposure:
        st.markdown("### Contexto epidemiológico")
        st.write(display_value(case.get("exposicion")))

    # -----------------------------------------------------
    # OBSERVACIONES
    # -----------------------------------------------------

    observations = case.get("observaciones", "")

    if observations:
        st.markdown("### Observaciones adicionales")
        st.write(observations)

    # -----------------------------------------------------
    # SIGNOS DE ALARMA
    # -----------------------------------------------------

    st.divider()
    st.markdown("### Evaluación de signos de alarma")

    warning_signs = case.get("signos_alarma", [])

    if warning_signs:
        st.error(
            "Se identifican hallazgos que requieren atención prioritaria."
        )

        for sign in warning_signs:
            st.markdown(f"- **{sign}**")

        if record_type == "prepared":

            if not st.session_state.get(
                "warning_acknowledged", False
            ):
                if st.button(
                    "Reconozco los signos de alarma",
                    type="primary",
                    key=f"acknowledge_{record_id}",
                    use_container_width=True
                ):
                    acknowledge_warning_signs()
                    st.rerun()

            else:
                st.success(
                    "Signos de alarma reconocidos. En un escenario real, "
                    "estos hallazgos requieren valoración clínica prioritaria."
                )

        else:
            st.warning(
                "Revisa estos hallazgos y considera la necesidad de "
                "valoración clínica prioritaria. Este expediente manual "
                "no se califica mediante el sistema de desafíos."
            )

    else:
        st.info(
            "No se han registrado signos de alarma en este expediente. "
            "Su ausencia no descarta una evolución clínica desfavorable."
        )

    # -----------------------------------------------------
    # RESULTADOS DE LABORATORIO
    # -----------------------------------------------------

    if record_type == "manual":

        lab_results = case.get("resultados_laboratorio", {})

        if lab_results:
            st.divider()
            st.markdown("### Resultados de laboratorio registrados")

            for test_name, result in lab_results.items():

                with st.expander(str(test_name)):

                    if isinstance(result, dict):
                        for key, value in result.items():
                            label = str(key).replace(
                                "_", " "
                            ).capitalize()

                            st.write(f"**{label}:** {value}")
                    else:
                        st.write(result)

                    if (
                        isinstance(result, dict)
                        and result.get("es_simulado")
                    ):
                        st.warning(
                            "Resultado generado para simulación académica."
                        )

                    elif isinstance(result, dict):
                        st.caption(
                            "Resultado introducido en el expediente."
                        )

    # -----------------------------------------------------
    # ANOTACIONES DEL INVESTIGADOR
    # -----------------------------------------------------

    st.divider()
    st.markdown("### Anotaciones del investigador")

    st.markdown(
        """
        <p class="patient-muted">
            Registra las hipótesis iniciales, hallazgos relevantes
            y aspectos que deseas comprobar durante la investigación.
        </p>
        """,
        unsafe_allow_html=True
    )

    note_key = f"note_{record_id}"
    current_note = case.get("nota_investigador", "")

    if note_key not in st.session_state:
        st.session_state[note_key] = current_note

    note = st.text_area(
        "Observaciones clínicas",
        key=note_key,
        height=140,
        placeholder=(
            "Registra tus observaciones, hipótesis y elementos "
            "que deseas contrastar mediante las pruebas..."
        ),
        label_visibility="collapsed"
    )

    if record_type == "manual":

        if st.button(
            "Guardar anotaciones",
            key=f"save_note_{record_id}"
        ):
            success, message = update_patient(
                record_id,
                {"nota_investigador": note}
            )

            if success:
                st.success(message)
            else:
                st.error(message)

    # -----------------------------------------------------
    # CONTINUACIÓN
    # -----------------------------------------------------

    st.divider()
    st.markdown("### Siguiente etapa")

    if record_type == "manual":
        st.write(
            "El expediente está listo para iniciar el análisis clínico "
            "y posteriormente registrar las pruebas de laboratorio."
        )
    else:
        st.write(
            "Continúa al laboratorio para seleccionar las pruebas "
            "que permitan contrastar tus hipótesis."
        )

    if st.button(
        "Continuar al laboratorio",
        type="primary",
        use_container_width=True,
        key=f"continue_lab_{record_id}"
    ):
        st.switch_page("pages/4_Laboratorio.py")

    st.divider()

    st.caption(
        "Nota académica: los casos y resultados preparados son simulados. "
        "La información introducida manualmente debe estar anonimizada. "
        "Esta aplicación no reemplaza la valoración médica ni los "
        "protocolos oficiales de diagnóstico y atención."
    )


# =========================================================
# MODALIDADES DE INVESTIGACIÓN
# =========================================================

st.markdown("## Modalidad de investigación")

mode = st.radio(
    "Selecciona cómo deseas trabajar",
    options=[
        "Registrar un paciente",
        "Casos preparados",
        "Pacientes registrados"
    ],
    horizontal=True,
    label_visibility="collapsed",
    key="patient_mode"
)

st.divider()


# =========================================================
# MODALIDAD 1: REGISTRO MANUAL
# =========================================================

if mode == "Registrar un paciente":

    st.markdown("## Nuevo expediente")

    st.markdown(
        """
        <p class="patient-muted">
            Introduce la información clínica y epidemiológica disponible.
            Los campos no obligatorios pueden quedar sin diligenciar
            cuando no se conozca el dato.
        </p>
        """,
        unsafe_allow_html=True
    )

    with st.form("patient_registration_form"):

        # INFORMACIÓN GENERAL

        st.markdown("### 1. Información general")

        col1, col2 = st.columns(2)

        with col1:
            patient_name = st.text_input(
                "Nombre o código del paciente *",
                placeholder="Ejemplo: PAC-001"
            )

            patient_age = st.number_input(
                "Edad en años *",
                min_value=0,
                max_value=120,
                value=25,
                step=1
            )

        with col2:
            patient_sex = st.selectbox(
                "Sexo",
                [
                    "No especificado",
                    "Femenino",
                    "Masculino",
                    "Otro"
                ]
            )

            evolution_days = st.number_input(
                "Días de evolución",
                min_value=0,
                max_value=365,
                value=1,
                step=1
            )

        consultation_reason = st.text_area(
            "Motivo de consulta",
            placeholder="Describe el motivo principal de consulta...",
            height=85
        )

        # SÍNTOMAS

        st.divider()
        st.markdown("### 2. Manifestaciones clínicas")

        common_symptoms = [
            "Fiebre",
            "Cefalea",
            "Dolor retroocular",
            "Mialgia",
            "Artralgia",
            "Exantema",
            "Prurito",
            "Náuseas",
            "Vómitos",
            "Diarrea",
            "Dolor abdominal",
            "Conjuntivitis",
            "Escalofríos",
            "Fatiga",
            "Dolor lumbar",
            "Sangrado",
            "Rigidez articular",
            "Fotofobia"
        ]

        selected_symptoms = st.multiselect(
            "Selecciona los síntomas presentes",
            options=common_symptoms,
            help="Puedes seleccionar varios síntomas."
        )

        other_symptoms = st.text_area(
            "Otros síntomas o manifestaciones",
            placeholder="Registra otros hallazgos clínicos...",
            height=75
        )

        # ANTECEDENTES

        st.divider()
        st.markdown("### 3. Antecedentes")

        history_options = [
            "Enfermedades crónicas",
            "Inmunosupresión",
            "Embarazo",
            "Viajes recientes",
            "Infección previa por arbovirus",
            "Vacunación contra fiebre amarilla",
            "Medicamentos recientes",
            "Antecedentes de dengue"
        ]

        selected_history = st.multiselect(
            "Antecedentes relevantes",
            options=history_options
        )

        other_history = st.text_area(
            "Otros antecedentes",
            placeholder="Describe otros antecedentes relevantes...",
            height=75
        )

        # EXPOSICIÓN EPIDEMIOLÓGICA

        st.divider()
        st.markdown("### 4. Contexto epidemiológico")

        exposure_options = [
            "Residencia en zona rural",
            "Residencia en zona urbana",
            "Viaje reciente",
            "Exposición a mosquitos",
            "Exposición a jejenes o pequeños dípteros",
            "Contacto con zonas selváticas",
            "Actividad agrícola",
            "Exposición a aguas potencialmente contaminadas",
            "Contacto con personas enfermas"
        ]

        selected_exposure = st.multiselect(
            "Factores de exposición",
            options=exposure_options
        )

        exposure_location = st.text_input(
            "Lugar de exposición o procedencia",
            placeholder="Ejemplo: municipio o departamento"
        )

        other_exposure = st.text_area(
            "Otros datos epidemiológicos",
            placeholder="Describe las condiciones de exposición...",
            height=75
        )

        # SIGNOS VITALES

        st.divider()
        st.markdown("### 5. Signos vitales")

        col1, col2 = st.columns(2)

        with col1:
            temperature = st.number_input(
                "Temperatura (°C)",
                min_value=0.0,
                max_value=45.0,
                value=0.0,
                step=0.1,
                format="%.1f",
                help="Deja 0 si no se dispone del dato."
            )

            heart_rate = st.number_input(
                "Frecuencia cardíaca (lpm)",
                min_value=0,
                max_value=300,
                value=0,
                step=1
            )

            respiratory_rate = st.number_input(
                "Frecuencia respiratoria (rpm)",
                min_value=0,
                max_value=100,
                value=0,
                step=1
            )

        with col2:
            systolic_pressure = st.number_input(
                "Presión sistólica (mmHg)",
                min_value=0,
                max_value=300,
                value=0,
                step=1
            )

            diastolic_pressure = st.number_input(
                "Presión diastólica (mmHg)",
                min_value=0,
                max_value=200,
                value=0,
                step=1
            )

            oxygen_saturation = st.number_input(
                "Saturación de oxígeno (%)",
                min_value=0,
                max_value=100,
                value=0,
                step=1
            )

        # SIGNOS DE ALARMA Y OBSERVACIONES

        st.divider()
        st.markdown("### 6. Hallazgos adicionales")

        alarm_options = [
            "Dolor abdominal intenso",
            "Vómitos persistentes",
            "Sangrado de mucosas",
            "Letargo o irritabilidad",
            "Acumulación de líquidos",
            "Dificultad respiratoria",
            "Disminución de la diuresis",
            "Hipotensión o signos de mala perfusión"
        ]

        selected_alarm_signs = st.multiselect(
            "Hallazgos de posible alarma",
            options=alarm_options,
            help=(
                "Selecciona únicamente hallazgos observados o "
                "documentados. La aplicación no sustituye su "
                "valoración clínica."
            )
        )

        additional_observations = st.text_area(
            "Observaciones adicionales",
            placeholder="Información complementaria del expediente...",
            height=100
        )

        # ENVÍO

        st.divider()

        submitted = st.form_submit_button(
            "Registrar paciente",
            type="primary",
            use_container_width=True
        )

    # -----------------------------------------------------
    # PROCESAMIENTO DEL REGISTRO
    # -----------------------------------------------------

    if submitted:

        if not patient_name.strip():
            st.error(
                "Debes introducir un nombre o código para identificar "
                "el expediente."
            )

        elif (
            (systolic_pressure > 0 and diastolic_pressure == 0)
            or (systolic_pressure == 0 and diastolic_pressure > 0)
        ):
            st.error(
                "Para registrar la presión arterial debes introducir "
                "tanto el valor sistólico como el diastólico."
            )

        else:

            vital_signs = {}

            if temperature > 0:
                vital_signs["temperatura"] = temperature

            if heart_rate > 0:
                vital_signs["frecuencia_cardiaca"] = heart_rate

            if respiratory_rate > 0:
                vital_signs["frecuencia_respiratoria"] = respiratory_rate

            if systolic_pressure > 0 and diastolic_pressure > 0:
                vital_signs["presion_arterial"] = (
                    f"{systolic_pressure}/{diastolic_pressure} mmHg"
                )

            if oxygen_saturation > 0:
                vital_signs["saturacion_oxigeno"] = oxygen_saturation

            symptoms = list(selected_symptoms)

            if other_symptoms.strip():
                symptoms.append(other_symptoms.strip())

            history = list(selected_history)

            if other_history.strip():
                history.append(other_history.strip())

            exposure = list(selected_exposure)

            if exposure_location.strip():
                exposure.append(
                    f"Lugar de exposición: {exposure_location.strip()}"
                )

            if other_exposure.strip():
                exposure.append(other_exposure.strip())

            patient_data = {
                "nombre": patient_name.strip(),
                "edad": int(patient_age),
                "sexo": patient_sex,
                "dia_evolucion": int(evolution_days),
                "motivo_consulta": consultation_reason.strip(),
                "sintomas": symptoms,
                "antecedentes": history,
                "exposicion": exposure,
                "signos_vitales": vital_signs,
                "signos_alarma": list(selected_alarm_signs),
                "observaciones": additional_observations.strip()
            }

            success, result = register_patient(patient_data)

            if success:
                st.success(
                    "Paciente registrado correctamente. "
                    "El expediente ya se encuentra activo."
                )

                st.info(
                    f"Identificador del expediente: {result}"
                )

                st.markdown(
                    "El expediente se muestra a continuación."
                )

            else:
                st.warning(result)


# =========================================================
# MODALIDAD 2: CASOS PREPARADOS
# =========================================================

elif mode == "Casos preparados":

    st.markdown("## Biblioteca de casos clínicos")

    st.markdown(
        """
        <p class="patient-muted">
            Selecciona uno de los escenarios preparados para desarrollar
            una investigación clínica guiada. Estos casos contienen
            resultados y diagnósticos configurados con fines educativos.
        </p>
        """,
        unsafe_allow_html=True
    )

    cases = load_cases()

    if not cases:
        st.warning(
            "No se encontraron casos clínicos. "
            "Verifica data/casos_clinicos.json."
        )

    else:

        case_ids = list(cases.keys())

        selected_id = st.selectbox(
            "Selecciona un caso clínico",
            options=case_ids,
            format_func=lambda key: (
                f"{key.upper()} — "
                f"{cases[key].get('titulo', 'Sin título')}"
            ),
            key="prepared_case_selector"
        )

        selected_case = cases[selected_id]

        st.markdown("### Resumen del escenario")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                "Edad",
                f"{selected_case.get('edad', 'N/D')} años"
            )

        with col2:
            st.metric(
                "Sexo",
                selected_case.get("sexo", "N/D")
            )

        with col3:
            st.metric(
                "Día de evolución",
                selected_case.get("dia_evolucion", "N/D")
            )

        st.write(
            selected_case.get(
                "motivo_consulta",
                "Sin motivo de consulta registrado."
            )
        )

        if st.button(
            "Abrir caso clínico",
            type="primary",
            use_container_width=True
        ):
            success = start_case(selected_id)

            if success:
                st.rerun()
            else:
                st.error(
                    "No fue posible abrir el caso seleccionado."
                )


# =========================================================
# MODALIDAD 3: PACIENTES REGISTRADOS
# =========================================================

elif mode == "Pacientes registrados":

    st.markdown("## Expedientes registrados")

    records = get_patient_records()

    if not records:
        st.info(
            "Todavía no hay pacientes registrados manualmente. "
            "Utiliza la opción «Registrar un paciente» para crear "
            "el primer expediente."
        )

    else:

        st.write(
            f"Total de expedientes manuales registrados: **{len(records)}**"
        )

        patient_ids = list(records.keys())

        selected_patient_id = st.selectbox(
            "Selecciona un expediente",
            options=patient_ids,
            format_func=lambda key: (
                f"{records[key].get('nombre', 'Sin nombre')} "
                f"— {records[key].get('edad', 'N/D')} años "
                f"— {key.upper()}"
            ),
            key="manual_patient_selector"
        )

        selected_patient = records[selected_patient_id]

        st.markdown("### Resumen del expediente")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                "Edad",
                f"{selected_patient.get('edad', 'N/D')} años"
            )

        with col2:
            st.metric(
                "Sexo",
                selected_patient.get("sexo", "N/D")
            )

        with col3:
            st.metric(
                "Día de evolución",
                selected_patient.get("dia_evolucion", "N/D")
            )

        if st.button(
            "Abrir expediente registrado",
            type="primary",
            use_container_width=True
        ):
            success = activate_patient(selected_patient_id)

            if success:
                st.rerun()
            else:
                st.error(
                    "No fue posible abrir este expediente."
                )


# =========================================================
# EXPEDIENTE ACTIVO
# =========================================================

active_case = get_active_case()
active_record_id = get_active_case_id()
active_record_type = get_active_record_type()

if active_case and active_record_id:
    show_patient_record(
        active_case,
        active_record_id,
        active_record_type
    )
