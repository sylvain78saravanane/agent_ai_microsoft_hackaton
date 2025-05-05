import streamlit as st
from streamlit_option_menu import option_menu
from utils.session_manager import logout_user, set_page
from utils.api import get_job_postings
from views.components import render_job_card, render_top_bar

def render_job_list():
    """Affiche la liste des offres d'emploi pour les candidats"""
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
        default_index=1,
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
    elif selected == "Mes candidatures":
        set_page("candidate_applications")
        st.rerun()
    
    # Titre de la page
    st.markdown("<h1 style='color: #00A8A8;'>Offres d'emploi disponibles</h1>", unsafe_allow_html=True)
    
    # Filtres de recherche
    with st.expander("Filtres de recherche", expanded=True):
        col1, col2, col3 = st.columns(3)
        
        with col1:
            secteur = st.selectbox(
                "Secteur", 
                ["Tous", "Technologie", "Finance", "Marketing", "Ressources humaines", "Juridique"]
            )
        
        with col2:
            contrat = st.selectbox(
                "Type de contrat", 
                ["Tous", "CDI", "CDD", "Stage", "Alternance", "Freelance"]
            )
        
        with col3:
            niveau = st.selectbox(
                "Niveau d'expérience", 
                ["Tous", "Débutant", "1-3 ans", "3-5 ans", "5-10 ans", "10+ ans"]
            )
        
        # Recherche par mots-clés
        search_query = st.text_input("Recherche par mots-clés", placeholder="Développeur, Python, Data...")
        
        st.markdown("<hr>", unsafe_allow_html=True)
    
    # Récupération des offres d'emploi
    try:
        # Appel à l'API pour récupérer les offres d'emploi
        response = get_job_postings()
        
        if isinstance(response, dict) and "error" in response:
            st.error(f"Erreur lors de la récupération des offres: {response['error']}")
            jobs = []
        else:
            jobs = response if isinstance(response, list) else []
        
        # Filtrage des offres selon les critères sélectionnés
        filtered_jobs = []
        for job in jobs:
            # Filtrer par secteur
            if secteur != "Tous" and job.get("secteur") != secteur:
                continue
            
            # Filtrer par type de contrat
            if contrat != "Tous" and job.get("contrat") != contrat:
                continue
            
            # Filtrer par niveau d'expérience (simplification)
            if niveau != "Tous" and niveau not in job.get("niveau", ""):
                continue
            
            # Filtrer par recherche textuelle
            if search_query and not (
                search_query.lower() in job.get("titre", "").lower() or
                search_query.lower() in job.get("content", "").lower() or
                any(search_query.lower() in comp.lower() for comp in job.get("competences", []))
            ):
                continue
            
            filtered_jobs.append(job)
        
        # Affichage des résultats
        st.markdown(f"<h3>{len(filtered_jobs)} offre(s) trouvée(s)</h3>", unsafe_allow_html=True)
        
        if not filtered_jobs:
            st.info("Aucune offre ne correspond à vos critères de recherche.")
        else:
            for job in filtered_jobs:
                job_data = {
                    "titre": job.get("titre", "Poste inconnu"),
                    "departement": job.get("secteur", "Secteur non spécifié"),
                    "type": job.get("contrat", "Type non spécifié"),
                    "localisation": "Paris",  # Valeur par défaut
                    "description": job.get("content", "")[:200] + "..." if job.get("content") else "",
                    "date_publication": job.get("date_publication", "Récemment"),
                    "salaire": "Selon profil",
                    "id": job.get("id", "")
                }
                
                render_job_card(job_data)
                
                col1, col2 = st.columns([4, 1])
                with col2:
                    if st.button("Voir détails", key=f"view_{job.get('id')}"):
                        st.session_state.selected_job = job
                        set_page("candidate_job_details")
                        st.rerun()
    except Exception as e:
        st.error(f"Une erreur s'est produite : {str(e)}")
        
if __name__ == "__main__":
    render_job_list()