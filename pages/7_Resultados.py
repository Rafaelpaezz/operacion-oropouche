
import streamlit as st

from utils.state import (
    initialize_state,
    load_cases,
    load_diseases,
    get_score,
    get_progress,
    reset_simulation
)

from utils.theme import apply_theme, page_header


# ---------------------------------------------------------
# CONFIGURACIÓN INICIAL
# ---------------------------------------------------------

st.set_page_config(
    page_title="Resultados | Operación Oropouche",
    page_icon="🏆",
    layout="wide"
)

initialize_state()
apply_theme("resultados")


# ---------------------------------------------------------
# ESTILOS DEL MÓDULO
# ---------------------------------------------------------

st.markdown(
    """
    <style>
    .results-intro {
        color: #53675B;
        font-size: 1rem;
        line-height: 1.65;
        max-width: 850px;
        margin-bottom: 1.2rem;
    }

    .results-label {
        color: #365D48;
        font-size: 0.76rem;
        font-weight: 700;
        letter-spacing: 0.10em;
        text-transform: uppercase;
        margin-bottom: 0.35rem;
    }

    .results-muted {
        color: #68776D;
        font-size: 0.88rem;
        line-height: 1.55;
    }

    .results-summary {
        background: rgba(255, 255, 255, 0.65);
        border: 1px solid rgba(85, 115, 90, 0.16);
        border-radius: 12px;
        padding: 1rem 1.1rem;
    }

    .results-case-title {
        color: #304A39;
        font-weight: 650;
    }
    </style>
    """,
    unsafe_allow_html=True
)


# ---------------------------------------------------------
# ENCABEZADO
# ---------------------------------------------------------

page_header(
    "Resultados de la investigación",
    "Consulta tu desempeño, revisa los expedientes resueltos "
    "y reconoce las oportunidades de mejora.",
    "MÓDULO 07 · EVALUACIÓN DEL DESEMPEÑO"
)

st.markdown(
    """
    <p class="results-intro">
        Este módulo reúne los resultados obtenidos durante la simulación.
        Revisa tus decisiones diagnósticas, identifica los aciertos y
        utiliza la retroalimentación para fortalecer tu razonamiento
        clínico y epidemiológico.
    </p>
    """,
    unsafe_allow_html=True
)


# ---------------------------------------------------------
# CARGA DE INFORMACIÓN
# ---------------------------------------------------------

cases = load_cases()
diseases = load_diseases()

if not cases:
    st.warning(
        "No se encontraron expedientes clínicos. "
        "Verifica el archivo data/casos_clinicos.json."
    )
    st.stop()

completed = st.session_state.get("completed_cases", [])
case_history = st.session_state.get("case_history", {})

if not isinstance(completed, (list, set, tuple)):
    completed = []

if not isinstance(case_history, dict):
    case_history = {}


# ---------------------------------------------------------
# CÁLCULO DE RESULTADOS
# ---------------------------------------------------------

total = len(cases)
completed_count = len(set(completed))
score = get_score()

progress = get_progress()

# La función get_progress() devuelve una proporción entre 0 y 1.
progress = max(0, min(float(progress), 1))

correct = sum(
    1
    for item in case_history.values()
    if item.get("correcto", False)
)

incorrect = sum(
    1
    for item in case_history.values()
    if not item.get("correcto", False)
)

progress_percentage = progress * 100


# ---------------------------------------------------------
# RESUMEN DE DESEMPEÑO
# ---------------------------------------------------------

st.markdown("### Resumen de desempeño")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Puntuación",
        score
    )

with col2:
    st.metric(
        "Casos completados",
        f"{completed_count}/{total}"
    )

with col3:
    st.metric(
        "Diagnósticos correctos",
        correct
    )

with col4:
    st.metric(
        "Diagnósticos incorrectos",
        incorrect
    )


# ---------------------------------------------------------
# PROGRESO GENERAL
# ---------------------------------------------------------

st.divider()

st.markdown("### Progreso de la investigación")

st.progress(progress)

st.write(
    f"Has completado el **{progress_percentage:.0f}%** "
    f"de los expedientes disponibles."
)

remaining = max(total - completed_count, 0)

if remaining == 0:
    st.success(
        "Has recorrido todos los expedientes disponibles."
    )
else:
    st.caption(
        f"Te quedan {remaining} expediente(s) por resolver."
    )


# ---------------------------------------------------------
# HISTORIAL DE EXPEDIENTES
# ---------------------------------------------------------

st.divider()

st.markdown("### Historial de expedientes")

if not case_history:

    st.info(
        "Todavía no has completado ningún desafío. "
        "Investiga un expediente para comenzar a generar resultados."
    )

else:

    for case_id, result in case_history.items():

        case = cases.get(case_id)

        if not case:
            continue

        diagnosis_id = result.get("diagnostico")

        diagnosis_data = diseases.get(
            diagnosis_id,
            {}
        ) if diagnosis_id else {}

        chosen_diagnosis = diagnosis_data.get(
            "nombre",
            diagnosis_id or "No registrado"
        )

        tests = result.get("pruebas", [])

        if not isinstance(tests, (list, dict, set, tuple)):
            tests = []

        is_correct = result.get("correcto", False)

        with st.container(border=True):

            col_info, col_status = st.columns([4, 1])

            with col_info:

                st.markdown(
                    f"#### {case.get('titulo', case_id)}"
                )

                st.caption(case_id.upper())

                st.write(
                    f"**Diagnóstico propuesto:** {chosen_diagnosis}"
                )

                st.write(
                    f"**Pruebas solicitadas:** {len(tests)}"
                )

                if result.get("signos_alarma_reconocidos"):
                    st.caption(
                        "Signos de alarma reconocidos."
                    )

            with col_status:

                if is_correct:
                    st.success("Correcto")
                else:
                    st.error("Incorrecto")

            # Información adicional disponible para el estudiante.
            correct_id = result.get("diagnostico_correcto")

            if correct_id in diseases:

                correct_name = diseases[correct_id].get(
                    "nombre",
                    correct_id
                )

                with st.expander("Consultar resultado del desafío"):

                    st.write(
                        f"**Diagnóstico esperado:** {correct_name}"
                    )

                    if not is_correct:
                        st.write(
                            "Revisa las manifestaciones, el contexto "
                            "epidemiológico y las pruebas diagnósticas "
                            "para identificar qué aspectos debes reforzar."
                        )


# ---------------------------------------------------------
# EVALUACIÓN DEL INVESTIGADOR
# ---------------------------------------------------------

st.divider()

st.markdown("### Evaluación del investigador")

if not case_history:

    st.write(
        "Completa al menos un expediente para consultar "
        "tu evaluación de desempeño."
    )

elif completed_count >= total and correct >= total:

    st.success(
        "Misión completada. Has resuelto correctamente todos "
        "los expedientes disponibles en esta versión."
    )

elif completed_count >= total:

    st.warning(
        "Has terminado todos los expedientes. Revisa los resultados "
        "y la retroalimentación para reforzar los conceptos que "
        "necesitas mejorar."
    )

else:

    st.info(
        "La investigación sigue en curso. Continúa con los expedientes "
        "pendientes para completar la misión."
    )


# ---------------------------------------------------------
# RECOMENDACIONES DE APRENDIZAJE
# ---------------------------------------------------------

st.divider()

st.markdown("### Recomendaciones de aprendizaje")

st.write(
    "Ten en cuenta los siguientes criterios al analizar "
    "los escenarios clínicos:"
)

recommendations = [
    "No bases el diagnóstico únicamente en la presencia de fiebre.",
    "Relaciona la exposición epidemiológica con los días de evolución.",
    "Compara las manifestaciones clínicas de las diferentes arbovirosis.",
    "Selecciona pruebas apropiadas y considera sus limitaciones.",
    "Reconoce los signos de alarma y prioriza la atención oportuna.",
    "Interpreta los resultados de laboratorio junto con el contexto clínico."
]

for recommendation in recommendations:
    st.markdown(f"- {recommendation}")


# ---------------------------------------------------------
# CONTROL DE LA SIMULACIÓN
# ---------------------------------------------------------

st.divider()

st.markdown("### Control de la simulación")

st.markdown(
    """
    <p class="results-muted">
        Puedes reiniciar la misión para comenzar una nueva investigación.
        Esta acción elimina la puntuación, los expedientes completados
        y el historial acumulado de la simulación.
    </p>
    """,
    unsafe_allow_html=True
)

if "confirm_reset" not in st.session_state:
    st.session_state.confirm_reset = False

if not st.session_state.confirm_reset:

    if st.button(
        "Reiniciar toda la misión",
        type="secondary",
        use_container_width=True
    ):
        st.session_state.confirm_reset = True
        st.rerun()

else:

    st.warning(
        "¿Estás seguro de que deseas reiniciar la misión? "
        "No podrás recuperar el progreso de esta sesión."
    )

    col_confirm, col_cancel = st.columns(2)

    with col_confirm:

        if st.button(
            "Sí, reiniciar misión",
            type="primary",
            use_container_width=True
        ):

            reset_simulation()
            st.rerun()

    with col_cancel:

        if st.button(
            "Cancelar",
            use_container_width=True
        ):

            st.session_state.confirm_reset = False
            st.rerun()


# ---------------------------------------------------------
# NOTA ACADÉMICA
# ---------------------------------------------------------

st.divider()

st.caption(
    "Los resultados y las puntuaciones corresponden a una simulación "
    "educativa. No representan indicadores epidemiológicos reales "
    "ni sustituyen la valoración clínica o los protocolos oficiales."
)
