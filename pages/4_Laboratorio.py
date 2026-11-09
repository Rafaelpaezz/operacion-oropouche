
import streamlit as st

from utils.state import (
    initialize_state,
    get_active_case,
    get_active_case_id,
    get_active_record_type,
    get_ordered_tests,
    get_lab_results,
    order_test,
    record_lab_result,
)

from utils.laboratory_engine import (
    get_all_tests,
    get_test,
    validate_test_request,
    interpret_test_result,
)

from utils.theme import apply_theme, page_header


# =========================================================
# CONFIGURACIÓN INICIAL
# =========================================================

st.set_page_config(
    page_title="Laboratorio diagnóstico | Operación Oropouche",
    page_icon="🧪",
    layout="wide"
)

initialize_state()
apply_theme("laboratorio")


# =========================================================
# ESTILOS DEL MÓDULO
# =========================================================

st.markdown(
    """
    <style>
    .lab-intro {
        color: #536771;
        font-size: 1rem;
        line-height: 1.65;
        max-width: 850px;
        margin-bottom: 1.2rem;
    }

    .lab-label {
        color: #285C73;
        font-size: 0.76rem;
        font-weight: 700;
        letter-spacing: 0.10em;
        text-transform: uppercase;
        margin-bottom: 0.35rem;
    }

    .lab-muted {
        color: #64747C;
        font-size: 0.88rem;
        line-height: 1.55;
    }

    .lab-result-title {
        color: #263F4A;
        font-weight: 650;
    }

    .lab-summary {
        background: rgba(255, 255, 255, 0.65);
        border: 1px solid rgba(80, 110, 125, 0.16);
        border-radius: 12px;
        padding: 1rem 1.1rem;
    }
    </style>
    """,
    unsafe_allow_html=True
)


# =========================================================
# FUNCIONES AUXILIARES
# =========================================================

def normalize_results(results):
    """
    Convierte los resultados del expediente en un diccionario
    organizado por identificador de prueba.
    """

    if isinstance(results, dict):
        normalized = {}

        for test_id, result in results.items():

            if isinstance(result, dict):
                normalized[str(test_id)] = result

        return normalized

    if isinstance(results, list):
        normalized = {}

        for result in results:

            if not isinstance(result, dict):
                continue

            test_id = (
                result.get("test_id")
                or result.get("id_prueba")
                or result.get("id")
            )

            if test_id:
                normalized[str(test_id)] = result

        return normalized

    return {}


def normalize_ordered_tests(tests):
    """
    Normaliza las pruebas solicitadas para permitir
    trabajar con listas o diccionarios.
    """

    if isinstance(tests, dict):
        return list(tests.keys())

    if isinstance(tests, (list, tuple, set)):
        normalized = []

        for item in tests:

            if isinstance(item, dict):
                test_id = (
                    item.get("test_id")
                    or item.get("id_prueba")
                    or item.get("id")
                )

                if test_id:
                    normalized.append(str(test_id))

            elif isinstance(item, str):
                normalized.append(item)

        return normalized

    return []


def is_prepared_record(record_type, case):
    """
    Identifica si el expediente corresponde a un caso preparado.
    """

    record_type = str(record_type or "").strip().lower()

    if record_type in {
        "prepared",
        "caso_preparado",
        "preparado",
        "case"
    }:
        return True

    if record_type in {
        "manual",
        "paciente_manual",
        "caso_libre",
        "libre"
    }:
        return False

    case_type = str(
        case.get("tipo_registro", case.get("origen", ""))
    ).strip().lower()

    return case_type in {
        "prepared",
        "caso_preparado",
        "preparado"
    }


def get_evolution_day(case):
    """
    Obtiene el día de evolución utilizando los nombres
    de campo disponibles en el expediente.
    """

    value = (
        case.get("dia_evolucion")
        or case.get("dias_evolucion")
        or case.get("dias_de_evolucion")
    )

    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def get_test_name(test_id, case_tests=None):
    """
    Obtiene el nombre de una prueba desde el catálogo
    o desde la configuración del caso preparado.
    """

    catalog_test = get_test(test_id)

    if catalog_test:
        return catalog_test.get("nombre", test_id)

    if isinstance(case_tests, dict):
        case_test = case_tests.get(test_id)

        if isinstance(case_test, dict):
            return case_test.get("nombre", test_id)

    return test_id


def show_result_status(result):
    """
    Presenta el resultado según su clasificación.
    """

    status = str(result.get("estado", "")).lower()

    result_text = result.get(
        "resultado",
        result.get("resultado_original", "Sin resultado")
    )

    if status == "positivo":
        st.warning(f"**Resultado positivo:** {result_text}")

    elif status == "negativo":
        st.success(f"**Resultado negativo:** {result_text}")

    elif status == "indeterminado":
        st.warning(f"**Resultado indeterminado:** {result_text}")

    elif status == "pendiente":
        st.info("**Estado:** Pendiente de resultado.")

    else:
        st.info(f"**Resultado registrado:** {result_text}")


# =========================================================
# ENCABEZADO
# =========================================================

page_header(
    "Laboratorio diagnóstico",
    "Selecciona las pruebas pertinentes y analiza los resultados "
    "obtenidos dentro del escenario clínico.",
    "MÓDULO 04 · ANÁLISIS DE LABORATORIO"
)

st.markdown(
    """
    <p class="lab-intro">
        La selección de pruebas debe considerar los síntomas, los
        antecedentes epidemiológicos y el día de evolución del paciente.
        La aplicación permite consultar pruebas disponibles, registrar
        solicitudes y analizar resultados de laboratorio.
    </p>
    """,
    unsafe_allow_html=True
)


# =========================================================
# VALIDACIÓN DEL EXPEDIENTE ACTIVO
# =========================================================

case = get_active_case()
active_case_id = get_active_case_id()
record_type = get_active_record_type()

if not isinstance(case, dict) or not case:

    st.warning(
        "No hay un expediente clínico activo. "
        "Debes seleccionar o registrar un paciente antes de "
        "solicitar pruebas."
    )

    if st.button(
        "Ir a expedientes clínicos",
        type="primary",
        use_container_width=True
    ):
        st.switch_page("pages/3_Pacientes.py")

    st.stop()


prepared_record = is_prepared_record(record_type, case)

if prepared_record:
    record_label = "CASO PREPARADO · RESULTADOS SIMULADOS"
else:
    record_label = "CASO LIBRE · REGISTRO DE RESULTADOS"


# =========================================================
# IDENTIFICACIÓN DEL EXPEDIENTE
# =========================================================

st.markdown(
    f"""
    <div class="lab-label">
        EXPEDIENTE ACTIVO · {str(active_case_id or "SIN ID").upper()}
    </div>
    """,
    unsafe_allow_html=True
)

st.subheader(
    case.get(
        "titulo",
        case.get("nombre", "Expediente clínico")
    )
)

st.caption(record_label)

evolution_day = get_evolution_day(case)

if evolution_day is not None:
    st.write(f"**Día de evolución:** {evolution_day}")
else:
    st.write("**Día de evolución:** No registrado")

if prepared_record:
    st.info(
        "Este escenario utiliza resultados ficticios configurados "
        "previamente para el entrenamiento."
    )
else:
    st.info(
        "Este expediente permite registrar resultados proporcionados "
        "por el usuario. La aplicación no genera resultados clínicos."
    )

st.divider()


# =========================================================
# RECUPERACIÓN DEL ESTADO DEL EXPEDIENTE
# =========================================================

ordered_tests = normalize_ordered_tests(
    get_ordered_tests()
)

results = normalize_results(
    get_lab_results()
)

case_tests = case.get("pruebas", {})

if not isinstance(case_tests, dict):
    case_tests = {}


# =========================================================
# CATÁLOGO Y SELECCIÓN DE PRUEBAS
# =========================================================

st.markdown("### Selección de pruebas")

st.write(
    "Selecciona las pruebas que consideres pertinentes para "
    "complementar el análisis clínico y epidemiológico."
)

catalog_tests = get_all_tests()

if prepared_record:

    # Los casos preparados conservan las pruebas definidas
    # específicamente en su archivo JSON.
    available_test_ids = list(case_tests.keys())

    if not available_test_ids:

        st.warning(
            "Este caso preparado no tiene pruebas de laboratorio "
            "configuradas en el archivo de casos clínicos."
        )

else:

    # Los expedientes libres utilizan el catálogo general.
    available_test_ids = [
        test["id"]
        for test in catalog_tests
        if isinstance(test, dict) and test.get("id")
    ]


# Evitar solicitar repetidamente pruebas ya registradas.
available_test_ids = [
    test_id
    for test_id in available_test_ids
    if test_id not in ordered_tests
]

if not available_test_ids:

    if ordered_tests:
        st.success(
            "Todas las pruebas disponibles para este expediente "
            "ya fueron solicitadas."
        )
    else:
        st.warning(
            "No hay pruebas disponibles para seleccionar."
        )

else:

    selected_tests = st.multiselect(
        "Pruebas disponibles",
        options=available_test_ids,
        format_func=lambda test_id: get_test_name(
            test_id,
            case_tests
        ),
        placeholder="Selecciona una o varias pruebas",
        key=f"lab_selection_{active_case_id}"
    )

    if selected_tests:

        st.caption(
            f"{len(selected_tests)} prueba(s) seleccionada(s)."
        )

        with st.expander("Consultar información de las pruebas"):

            for test_id in selected_tests:

                test_info = get_test(test_id)

                if not test_info and isinstance(
                    case_tests.get(test_id), dict
                ):
                    test_info = case_tests[test_id]

                if not isinstance(test_info, dict):
                    test_info = {}

                st.markdown(
                    f"**{get_test_name(test_id, case_tests)}**"
                )

                if test_info.get("metodo"):
                    st.write(
                        f"**Método:** {test_info['metodo']}"
                    )

                if test_info.get("tipo_muestra"):
                    st.write(
                        f"**Tipo de muestra:** "
                        f"{test_info['tipo_muestra']}"
                    )

                if test_info.get("objetivo"):
                    st.write(
                        f"**Objetivo:** {test_info['objetivo']}"
                    )

                if test_info.get("consideraciones"):
                    st.caption(test_info["consideraciones"])

                # Orientación temporal para expedientes libres.
                if not prepared_record and evolution_day is not None:

                    validation = validate_test_request(
                        test_id,
                        evolution_day
                    )

                    if validation.get("valido"):

                        st.caption(
                            validation.get("mensaje", "")
                        )

                st.divider()

    request_tests = st.button(
        "Solicitar pruebas seleccionadas",
        type="primary",
        use_container_width=True,
        disabled=not selected_tests
    )

    if request_tests:

        messages = []
        errors = []

        for test_id in selected_tests:

            success, message = order_test(test_id)

            if success:
                messages.append(message)
            else:
                errors.append(message)

        if messages:
            st.session_state[
                f"last_lab_message_{active_case_id}"
            ] = " ".join(messages)

        if errors:
            st.session_state[
                f"last_lab_error_{active_case_id}"
            ] = " ".join(errors)

        st.rerun()


# =========================================================
# MENSAJES DE SOLICITUD
# =========================================================

message_key = f"last_lab_message_{active_case_id}"
error_key = f"last_lab_error_{active_case_id}"

last_message = st.session_state.get(message_key)
last_error = st.session_state.get(error_key)

if last_message:
    st.success(last_message)

if last_error:
    st.error(last_error)


# =========================================================
# ACTUALIZAR INFORMACIÓN DEL EXPEDIENTE
# =========================================================

ordered_tests = normalize_ordered_tests(
    get_ordered_tests()
)

results = normalize_results(
    get_lab_results()
)


# =========================================================
# REGISTRO MANUAL DE RESULTADOS
# =========================================================

if not prepared_record:

    st.divider()

    st.markdown("### Registro de resultados")

    st.markdown(
        """
        <p class="lab-muted">
            Registra el resultado tal como aparece en el informe
            del laboratorio. Puedes ingresar resultados cualitativos
            o valores reportados por el laboratorio.
        </p>
        """,
        unsafe_allow_html=True
    )

    pending_tests = [
        test_id
        for test_id in ordered_tests
        if test_id not in results
        or not results[test_id].get("resultado")
    ]

    if not pending_tests:

        if ordered_tests:
            st.success(
                "Todas las pruebas solicitadas tienen un resultado "
                "registrado."
            )
        else:
            st.info(
                "Primero debes solicitar una prueba para poder "
                "registrar su resultado."
            )

    else:

        for test_id in pending_tests:

            test_info = get_test(test_id) or {}

            test_name = test_info.get("nombre", test_id)

            with st.expander(
                f"Registrar resultado · {test_name}",
                expanded=len(pending_tests) == 1
            ):

                st.write(
                    f"**Método:** "
                    f"{test_info.get('metodo', 'No especificado')}"
                )

                st.write(
                    f"**Muestra:** "
                    f"{test_info.get('tipo_muestra', 'No especificada')}"
                )

                with st.form(
                    key=f"result_form_{active_case_id}_{test_id}"
                ):

                    raw_result = st.text_area(
                        "Resultado reportado por el laboratorio",
                        placeholder=(
                            "Ejemplo: Positivo, Negativo, "
                            "No detectado o valor reportado..."
                        ),
                        key=f"raw_result_{active_case_id}_{test_id}"
                    )

                    submitted = st.form_submit_button(
                        "Guardar resultado",
                        type="primary",
                        use_container_width=True
                    )

                    if submitted:

                        if not raw_result.strip():

                            st.error(
                                "Debes ingresar el resultado antes "
                                "de guardarlo."
                            )

                        else:

                            result_data = {
                                "resultado": raw_result.strip(),
                                "es_simulado": False,
                                "origen": "registro_manual"
                            }

                            interpretation = interpret_test_result(
                                test_id,
                                result_data
                            )

                            result_data.update({
                                "estado": interpretation.get(
                                    "estado",
                                    "no_clasificado"
                                ),
                                "interpretacion": interpretation.get(
                                    "interpretacion",
                                    "Resultado registrado. "
                                    "Requiere revisión del informe."
                                ),
                                "metodo": test_info.get(
                                    "metodo",
                                    "No especificado"
                                ),
                                "nombre": test_name
                            })

                            if not interpretation.get("valido"):

                                st.error(
                                    interpretation.get(
                                        "interpretacion",
                                        "No fue posible interpretar "
                                        "el resultado."
                                    )
                                )

                            else:

                                saved = record_lab_result(
                                    test_id,
                                    result_data
                                )

                                if (
                                    isinstance(saved, tuple)
                                    and len(saved) >= 2
                                ):

                                    save_success, save_message = saved

                                    if save_success:
                                        st.success(save_message)
                                    else:
                                        st.error(save_message)

                                else:

                                    st.success(
                                        "Resultado registrado "
                                        "en el expediente."
                                    )

                                st.rerun()


# =========================================================
# RESULTADOS DE LABORATORIO
# =========================================================

st.divider()

st.markdown("### Resultados de laboratorio")

results = normalize_results(
    get_lab_results()
)

if not results:

    st.info(
        "Todavía no hay resultados disponibles para este expediente. "
        "Solicita las pruebas correspondientes y registra los resultados "
        "cuando estén disponibles."
    )

else:

    st.markdown(
        """
        <p class="lab-muted">
            Revisa cada resultado junto con su interpretación.
            Considera el método utilizado, el momento de toma de muestra
            y el contexto clínico y epidemiológico.
        </p>
        """,
        unsafe_allow_html=True
    )

    for test_id, result in results.items():

        if not isinstance(result, dict):
            continue

        test_name = result.get(
            "nombre",
            get_test_name(test_id, case_tests)
        )

        result_text = result.get(
            "resultado",
            result.get("resultado_original", "Sin resultado")
        )

        interpretation = result.get(
            "interpretacion",
            "No se registró una interpretación para esta prueba."
        )

        with st.container(border=True):

            st.markdown(f"#### {test_name}")

            show_result_status(result)

            st.markdown("**Interpretación**")
            st.write(interpretation)

            method = result.get("metodo")

            if method:
                st.caption(f"Método: {method}")

            sample_date = result.get(
                "fecha",
                result.get("fecha_registro")
            )

            if sample_date:
                st.caption(f"Fecha de registro: {sample_date}")

            if result.get("es_simulado", False):
                st.caption(
                    "Resultado ficticio utilizado exclusivamente "
                    "para entrenamiento."
                )
            else:
                st.caption(
                    "Resultado registrado en el expediente."
                )


# =========================================================
# RESUMEN DE LA INVESTIGACIÓN
# =========================================================

st.divider()

st.markdown("### Resumen de investigación")

ordered_tests = normalize_ordered_tests(
    get_ordered_tests()
)

results = normalize_results(
    get_lab_results()
)

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Pruebas solicitadas",
        len(ordered_tests)
    )

with col2:
    st.metric(
        "Resultados disponibles",
        len(results)
    )

with col3:
    st.metric(
        "Pruebas pendientes",
        max(len(ordered_tests) - len(results), 0)
    )


# =========================================================
# CONSIDERACIONES ACADÉMICAS
# =========================================================

st.divider()

st.markdown("### Consideraciones para la interpretación")

if prepared_record:

    st.warning(
        "Este expediente utiliza resultados ficticios y "
        "preconfigurados para el entrenamiento académico. "
        "No corresponden a un paciente real."
    )

else:

    st.warning(
        "Los resultados de este expediente son registrados por "
        "el usuario. La clasificación automática es orientativa "
        "y no sustituye la interpretación del informe original "
        "por parte de un profesional."
    )

st.markdown(
    """
    <p class="lab-muted">
        Las ventanas temporales del catálogo son orientativas.
        La selección y la interpretación de las pruebas deben considerar
        el tipo de muestra, el momento de recolección, las características
        del ensayo y los protocolos oficiales aplicables.
    </p>
    """,
    unsafe_allow_html=True
)


# =========================================================
# NAVEGACIÓN
# =========================================================

st.divider()

st.markdown("### Siguiente etapa")

st.write(
    "Con los resultados disponibles, continúa a los desafíos "
    "diagnósticos para contrastar tus hipótesis y justificar "
    "la enfermedad que consideras más probable."
)

if st.button(
    "Continuar a los desafíos diagnósticos",
    type="primary",
    use_container_width=True
):
    st.switch_page("pages/6_Desafios.py")
