import streamlit as st
from streamlit_option_menu import option_menu
from utils.session_manager import set_page
from views.components import render_top_bar

def render_applications():
    """Affiche les candidatures de l'utilisateur"""
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
        default_index=2,
        orientation="horizontal",
        styles={
            "container": {"padding": "0!important", "background-color": "#1E1E1E"},
            "icon": {"color": "#00A8A8", "font-size": "14px"},
            "nav-link": {"font-size": "14px", "text-align": "center", "margin": "0px", "--hover-color": "#2A2A2A"},
            "nav-link-selected": {"background-color": "#006666"},
        }
    )
    
    # Redirection si on change d'onglet
    if selected == "Accueil":
        set_page("candidate_home")
        st.rerun()
    elif selected == "Offres d'emploi":
        set_page("candidate_jobs")
        st.rerun()
    
    # Titre de la page
    st.markdown("<h1 style='color: #00A8A8;'>Mes candidatures</h1>", unsafe_allow_html=True)
    
    # Récupération des candidatures (cette partie serait idéalement liée à une API)
    # Pour l'instant, nous affichons des données fictives
    
    # Note: En réalité, il faudrait appeler une API pour récupérer les candidatures de l'utilisateur
    # en utilisant leur email comme identifiant
    user_email = st.session_state.user.get("userEmail", "")
    
    # Candidatures fictives pour la démo
    applications = [
        {
            "id": "app_123",
            "job_title": "Développeur Frontend React",
            "company": "HiRo Site",
            "date": "01/05/2025",
            "status": "En cours d'analyse",
            "match_score": 85
        },
        {
            "id": "app_124",
            "job_title": "Data Scientist Senior",
            "company": "HiRo Site",
            "date": "28/04/2025",
            "status": "Entretien planifié",
            "match_score": 92
        }
    ]
    
    if not applications:
        st.info("Vous n'avez pas encore postulé à des offres d'emploi.")
        
        # Bouton pour consulter les offres
        if st.button("Consulter les offres d'emploi"):
            set_page("candidate_jobs")
            st.rerun()
    else:
        # Affichage des candidatures
        for app in applications:
            with st.container():
                st.markdown(f"""
                <div style="background-color: #1E1E1E; border-radius: 10px; padding: 15px; margin-bottom: 15px; border: 1px solid #333333;">
                    <h3 style="color: #00A8A8; margin-top: 0;">{app['job_title']}</h3>
                    <p><strong>Entreprise:</strong> {app['company']}</p>
                    <p><strong>Date de candidature:</strong> {app['date']}</p>
                    <p><strong>Statut:</strong> 
                        <span style="background-color: {'#004D40' if app['status'] == 'Entretien planifié' else '#2A2A2A'}; 
                                    padding: 4px 10px; 
                                    border-radius: 10px;">
                            {app['status']}
                        </span>
                    </p>
                    <p><strong>Score de matching:</strong> 
                        <span style="color: {'#00BFA5' if app['match_score'] >= 80 else '#FFAB40'}; font-weight: bold;">
                            {app['match_score']}%
                        </span>
                    </p>
                </div>
                """, unsafe_allow_html=True)
                
                col1, col2 = st.columns([4, 1])
                with col2:
                    st.button("Voir détails", key=f"view_app_{app['id']}")
    
    # Suggestion d'autres offres
    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("<h3>Offres qui pourraient vous intéresser</h3>", unsafe_allow_html=True)
    
    # Offres suggérées fictives
    suggested_jobs = [
        {
            "id": "job_789",
            "titre": "Lead Developer Python",
            "departement": "Technologie",
            "type": "CDI", 
            "localisation": "Paris",
            "match_score": 88
        },
        {
            "id": "job_790",
            "titre": "Architecte Cloud",
            "departement": "Infrastructure",
            "type": "CDI",
            "localisation": "Paris",
            "match_score": 75
        }
    ]
    
    col1, col2 = st.columns(2)
    
    for i, job in enumerate(suggested_jobs):
        with col1 if i % 2 == 0 else col2:
            st.markdown(f"""
            <div style="background-color: #1E1E1E; border-radius: 10px; padding: 15px; margin-bottom: 15px; border: 1px solid #333333;">
                <h3 style="color: #00A8A8; margin-top: 0;">{job['titre']}</h3>
                <p><strong>Secteur:</strong> {job['departement']} | <strong>Type:</strong> {job['type']}</p>
                <p><strong>Match avec votre profil:</strong> 
                    <span style="color: {'#00BFA5' if job['match_score'] >= 80 else '#FFAB40'}; font-weight: bold;">
                        {job['match_score']}%
                    </span>
                </p>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button("Voir l'offre", key=f"view_suggested_{job['id']}"):
                # En situation réelle, il faudrait récupérer les détails du job
                # et les stocker dans st.session_state.selected_job
                st.session_state.selected_job = job
                set_page("candidate_job_details")
                st.rerun()

if __name__ == "__main__":
    render_applications()