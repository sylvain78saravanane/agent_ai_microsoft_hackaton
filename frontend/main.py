import streamlit as st
import sys
import os

# Ajouter les répertoires au chemin Python
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)
sys.path.append(current_dir)

# Import des utilitaires
from utils.session_manager import initialize_session_state, set_page
from utils.styles import load_css

def main():
    """
    Point d'entrée principal de l'application HiRo.
    """
    # Configuration de la page
    st.set_page_config(
        page_title="HiRo - Assistant RH Intelligent",
        page_icon="👔",
        layout="wide",
        initial_sidebar_state="collapsed"
    )
    
    # Initialiser la session et charger les styles CSS
    initialize_session_state()
    load_css()
    
    # Logique de routage selon la page actuelle
    if "current_page" not in st.session_state:
        st.session_state.current_page = "login"
    
    # Router vers la vue appropriée
    if st.session_state.current_page == "login":
        from views.login_view import render_login_view
        render_login_view()
    
    # Portail Candidat
    elif st.session_state.current_page == "candidate_home":
        from views.candidate_portal.home import render_candidate_home
        render_candidate_home()
    elif st.session_state.current_page == "candidate_jobs":
        from views.candidate_portal.job_list import render_job_list
        render_job_list()
    elif st.session_state.current_page == "candidate_job_details":
        from views.candidate_portal.job_details import render_job_details
        render_job_details()
    elif st.session_state.current_page == "candidate_applications":
        from views.candidate_portal.applications import render_applications
        render_applications()
    
    # Portail Recruteur
    elif st.session_state.current_page == "recruiter_dashboard":
        from views.recruiter_portal.dashboard import render_recruiter_dashboard
        render_recruiter_dashboard()
    elif st.session_state.current_page == "recruiter_job_postings":
        from views.recruiter_portal.job_management import render_job_management
        render_job_management()
    elif st.session_state.current_page == "recruiter_job_details":
        from views.recruiter_portal.job_management import render_job_details as render_recruiter_job_details
        render_recruiter_job_details()
    elif st.session_state.current_page == "recruiter_applications":
        from views.recruiter_portal.candidat_management import render_candidate_management
        render_candidate_management()
    elif st.session_state.current_page == "recruiter_candidate_details":
        from views.recruiter_portal.candidat_management import render_candidate_details
        render_candidate_details()
    elif st.session_state.current_page == "recruiter_candidate_analysis":
        from views.recruiter_portal.candidat_management import render_candidate_analysis
        render_candidate_analysis()
    elif st.session_state.current_page == "recruiter_chatbot":
        from views.recruiter_portal.chatbot import render_chatbot
        render_chatbot()
    
    else:
        # Page par défaut si non reconnue
        st.error(f"Page non reconnue: {st.session_state.current_page}")
        set_page("login")
        st.rerun()

if __name__ == "__main__":
    main()