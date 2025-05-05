import streamlit as st
from streamlit_option_menu import option_menu
from utils.session_manager import logout_user, set_page
from utils.api import get_job_postings
from views.components import render_job_card, render_top_bar

def render_candidate_home():
    """Affiche la page d'accueil du portail candidat"""
    if "user" not in st.session_state or not st.session_state.user:
        set_page("login")
        st.rerun()
        return
    
    render_top_bar()
    
    # Navigation horizontale
    selected = option_menu(
        menu_title=None,
        options=["Accueil", "Offres d'emploi", "Mes candidatures"],
        icons=["house", "briefcase", "person-lines-fill"],
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
    
    # Contenu selon la navigation sélectionnée
    if selected == "Accueil":
        _render_home_content()
    elif selected == "Offres d'emploi":
        set_page("candidate_jobs")
        st.rerun()
    elif selected == "Mes candidatures":
        set_page("candidate_applications")
        st.rerun()

def _render_home_content():
    """Affiche le contenu principal de la page d'accueil"""
    # Message de bienvenue
    st.markdown(f"""
    <h1 style="color: #00A8A8;">Bienvenue, {st.session_state.user.get('prenom', '')} !</h1>
    <p style="font-size: 18px; margin-bottom: 30px;">
        Trouvez l'opportunité qui correspond à vos compétences et vos aspirations.
    </p>
    """, unsafe_allow_html=True)
    
    # Statistiques
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
        <div class="stat-card">
            <div class="stat-label">Offres disponibles</div>
            <div class="stat-value">12</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="stat-card">
            <div class="stat-label">Vos candidatures</div>
            <div class="stat-value">2</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="stat-card">
            <div class="stat-label">Entretiens planifiés</div>
            <div class="stat-value">1</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Offres d'emploi récentes
    st.markdown("<h2 style='margin-top: 40px;'>Dernières offres d'emploi</h2>", unsafe_allow_html=True)
    
    try:
        # Récupérer les offres d'emploi via l'API
        response = get_job_postings()
        
        if isinstance(response, dict) and "error" in response:
            st.error(f"Erreur lors de la récupération des offres: {response['error']}")
            jobs = []
        else:
            jobs = response if isinstance(response, list) else []
        
        # Afficher les offres récentes (limité à 2)
        if not jobs:
            st.info("Aucune offre d'emploi disponible pour le moment.")
        else:
            recent_jobs = jobs[:min(2, len(jobs))]
            
            col1, col2 = st.columns(2)
            
            for i, job in enumerate(recent_jobs):
                with col1 if i % 2 == 0 else col2:
                    job_data = {
                        "titre": job.get("titre", "Poste inconnu"),
                        "departement": job.get("secteur", "Secteur non spécifié"),
                        "type": job.get("contrat", "Type non spécifié"),
                        "localisation": "Paris",  # Valeur par défaut
                        "description": job.get("content", "")[:150] + "..." if job.get("content") else "",
                        "date_publication": job.get("date_publication", "Récemment"),
                        "salaire": "Selon profil",
                        "id": job.get("id", "")
                    }
                    
                    render_job_card(job_data)
                    
                    # Bouton pour voir les détails
                    if st.button(f"Voir détails", key=f"view_{job.get('id', i)}"):
                        st.session_state.selected_job = job
                        set_page("candidate_job_details")
                        st.rerun()
        
        # Bouton pour voir toutes les offres
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("Voir toutes les offres d'emploi", use_container_width=True):
                set_page("candidate_jobs")
                st.rerun()
    
    except Exception as e:
        st.error(f"Une erreur s'est produite : {str(e)}")
        
    # Section Ressources
    st.markdown("<h2 style='margin-top: 40px;'>Ressources pour votre recherche</h2>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="job-card">
            <h3>Conseils pour votre CV</h3>
            <p>Optimisez votre CV pour maximiser vos chances d'être remarqué par les recruteurs.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="job-card">
            <h3>Préparer votre entretien</h3>
            <p>Des techniques et astuces pour réussir vos entretiens d'embauche.</p>
        </div>
        """, unsafe_allow_html=True)

if __name__ == "__main__":
    render_candidate_home()