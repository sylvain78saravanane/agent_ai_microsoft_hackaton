import streamlit as st
from streamlit_option_menu import option_menu
import sys
import os

# Ajout des chemins d'importation pour résoudre les problèmes
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(os.path.dirname(current_dir))
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

# Importation simplifiée
from utils.session_manager import set_page

def render_recruiter_dashboard():
    """Affiche le tableau de bord pour les recruteurs"""
    if "user" not in st.session_state or not st.session_state.user:
        set_page("login")
        st.rerun()
        return
    
    render_top_bar()
    
    # Navigation horizontale
    selected = option_menu(
        menu_title=None,
        options=["Tableau de bord", "Fiches de poste", "Candidatures", "Chatbot HiRo"],
        icons=["columns-gap", "file-earmark-text", "people", "chat-dots"],
        menu_icon="cast",
        default_index=0,
        orientation="horizontal",
        styles={
            "container": {"padding": "0!important", "background-color": "#1E1E1E"},
            "icon": {"color": "#00A8A8", "font-size": "14px"},
            "nav-link": {"font-size": "14px", "text-align": "center", "margin": "0px", "--hover-color": "#2A2A2A"},
            "nav-link-selected": {"background-color": "#006666"},
        }
    )
    
    # Redirection si on change d'onglet
    if selected == "Fiches de poste":
        set_page("recruiter_job_postings")
        st.rerun()
    elif selected == "Candidatures":
        set_page("recruiter_applications")
        st.rerun()
    elif selected == "Chatbot HiRo":
        set_page("recruiter_chatbot")
        st.rerun()
    
    # Titre et message de bienvenue
    st.markdown(f"""
    <h1 style="color: #00A8A8;">Bienvenue, {st.session_state.user.get('prenom', '')} !</h1>
    <p style="font-size: 18px; margin-bottom: 30px;">
        Votre tableau de bord RH vous permet de piloter vos recrutements efficacement.
    </p>
    """, unsafe_allow_html=True)
    
    # Statistiques
    render_dashboard_stats()
    
    # Actions rapides
    st.markdown("<h2 style='margin-top: 40px;'>Actions rapides</h2>", unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div style="background-color: #1E1E1E; padding: 20px; border-radius: 10px; text-align: center; height: 150px; border: 1px solid #333333;">
            <div style="font-size: 36px; color: #00A8A8; margin-bottom: 15px;">
                <i class="fas fa-file-alt"></i>
                ✨
            </div>
            <p style="margin-bottom: 15px;">Créer une fiche de poste</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("Créer fiche", key="create_fiche_btn"):
            set_page("recruiter_chatbot")  # Rediriger vers le chatbot pour la création
            st.rerun()
    
    with col2:
        st.markdown("""
        <div style="background-color: #1E1E1E; padding: 20px; border-radius: 10px; text-align: center; height: 150px; border: 1px solid #333333;">
            <div style="font-size: 36px; color: #00A8A8; margin-bottom: 15px;">
                <i class="fas fa-search"></i>
                🔍
            </div>
            <p style="margin-bottom: 15px;">Rechercher des candidats</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("Rechercher", key="search_candidates_btn"):
            set_page("recruiter_applications")
            st.rerun()
    
    with col3:
        st.markdown("""
        <div style="background-color: #1E1E1E; padding: 20px; border-radius: 10px; text-align: center; height: 150px; border: 1px solid #333333;">
            <div style="font-size: 36px; color: #00A8A8; margin-bottom: 15px;">
                <i class="fas fa-chart-line"></i>
                📊
            </div>
            <p style="margin-bottom: 15px;">Voir les rapports</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("Rapports", key="reports_btn"):
            st.info("Fonctionnalité à venir")
    
    with col4:
        st.markdown("""
        <div style="background-color: #1E1E1E; padding: 20px; border-radius: 10px; text-align: center; height: 150px; border: 1px solid #333333;">
            <div style="font-size: 36px; color: #00A8A8; margin-bottom: 15px;">
                <i class="fas fa-robot"></i>
                🤖
            </div>
            <p style="margin-bottom: 15px;">Discuter avec HiRo</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("Chatbot", key="chatbot_btn"):
            set_page("recruiter_chatbot")
            st.rerun()
    
    # Candidatures récentes
    st.markdown("<h2 style='margin-top: 40px;'>Candidatures récentes</h2>", unsafe_allow_html=True)
    
    # Données fictives pour les candidatures récentes
    recent_applications = [
        {
            "id": "app_001",
            "nom": "Dupont",
            "prenom": "Marie",
            "poste": "Data Scientist Senior",
            "date": "05/05/2025",
            "matching": 92
        },
        {
            "id": "app_002",
            "nom": "Martin",
            "prenom": "Thomas",
            "poste": "Développeur Frontend React",
            "date": "04/05/2025",
            "matching": 85
        },
        {
            "id": "app_003",
            "nom": "Lefebvre",
            "prenom": "Julie",
            "poste": "Chef de Projet IT",
            "date": "02/05/2025",
            "matching": 78
        }
    ]
    
    if not recent_applications:
        st.info("Aucune candidature récente à afficher.")
    else:
        for app in recent_applications:
            st.markdown(f"""
            <div style="background-color: #1E1E1E; border-radius: 10px; padding: 15px; margin-bottom: 15px; border: 1px solid #333333;">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <h3 style="color: #00A8A8; margin-top: 0;">{app['prenom']} {app['nom']}</h3>
                        <p><strong>Poste:</strong> {app['poste']}</p>
                        <p><strong>Date:</strong> {app['date']}</p>
                    </div>
                    <div style="text-align: center; padding: 10px; background-color: {'#004D40' if app['matching'] >= 80 else '#2A2A2A'}; border-radius: 50%; width: 60px; height: 60px; display: flex; align-items: center; justify-content: center;">
                        <span style="font-size: 20px; font-weight: bold; color: {'#00BFA5' if app['matching'] >= 80 else '#FFAB40'};">
                            {app['matching']}%
                        </span>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            col1, col2 = st.columns([4, 1])
            with col2:
                if st.button("Voir CV", key=f"view_cv_{app['id']}"):
                    # En situation réelle, cette action ouvrirait les détails du candidat
                    # et de sa candidature
                    st.session_state.selected_candidate = app
                    set_page("recruiter_candidate_details")
                    st.rerun()
    
    # Section Assistant HiRo
    st.markdown("<h2 style='margin-top: 40px;'>Assistant HiRo</h2>", unsafe_allow_html=True)
    
    st.markdown("""
    <div style="background-color: #1E1E1E; border-radius: 10px; padding: 20px; margin-bottom: 20px; border: 1px solid #333333;">
        <div style="display: flex; align-items: center;">
            <div style="margin-right: 20px; font-size: 40px;">🤖</div>
            <div>
                <h3 style="color: #00A8A8; margin-top: 0;">Besoin d'assistance pour vos recrutements ?</h3>
                <p>Utilisez HiRo pour générer des fiches de poste, analyser des CV ou obtenir des recommandations de candidats.</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("Accéder à l'assistant HiRo", use_container_width=True):
        set_page("recruiter_chatbot")
        st.rerun()

def render_top_bar():
    """Affiche la barre de navigation supérieure."""
    col1, col2, col3 = st.columns([1, 3, 1])
    
    with col1:
        st.image("https://i.ibb.co/f4Kq0hP/logo-hiro.png", width=100)  # Placeholder pour un logo
    
    with col2:
        st.markdown("""
        <h1 style='text-align: center; color: #2E86C1;'>HiRo - Assistant RH Intelligent</h1>
        """, unsafe_allow_html=True)
    
    with col3:
        if "user" in st.session_state and st.session_state.user:
            if st.button("📤 Déconnexion"):
                from utils.session_manager import logout_user
                logout_user()
                st.rerun()

def render_dashboard_stats():
    """Affiche les statistiques du tableau de bord en dark mode."""
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="stat-card">
            <div class="stat-label">Postes Ouverts</div>
            <div class="stat-value">12</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="stat-card">
            <div class="stat-label">Candidatures Reçues</div>
            <div class="stat-value">87</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="stat-card">
            <div class="stat-label">Entretiens Planifiés</div>
            <div class="stat-value">9</div>
        </div>
        """, unsafe_allow_html=True)

if __name__ == "__main__":
    render_recruiter_dashboard()