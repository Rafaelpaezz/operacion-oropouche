
import streamlit as st


def initialize_state():
    """Inicializa la información compartida de la aplicación."""

    defaults = {
        "patients": [],
        "selected_patient": None,
        "lab_results": [],
        "challenge_score": 0,
        "challenges_completed": [],
        "total_attempts": 0,
        "ai_messages": [],
        "user_name": "Estudiante",
        "simulation_started": False,
    }

    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def add_patient(patient):
    """Registra un paciente en la simulación."""
    st.session_state.patients.append(patient)


def add_lab_result(result):
    """Guarda un resultado de laboratorio."""
    st.session_state.lab_results.append(result)


def complete_challenge(challenge_id, points):
    """Registra un desafío completado sin duplicarlo."""
    if challenge_id not in st.session_state.challenges_completed:
        st.session_state.challenges_completed.append(challenge_id)
        st.session_state.challenge_score += points
        st.session_state.total_attempts += 1


def get_progress():
    """Calcula el progreso de los desafíos."""
    completed = len(st.session_state.challenges_completed)
    total = 5

    return min(completed / total, 1.0)
