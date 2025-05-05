import streamlit as st
import base64
from streamlit_option_menu import option_menu
from utils.session_manager import set_page
from utils.api import get_job_postings
from views.components import render_top_bar, render_job_card

def render_job_management():
    """Affiche la gestion des fiches de poste pour les recruteurs"""
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
    if selected == "Tableau de bord":
        set_page("recruiter_dashboard")
        st.rerun()
    elif selected == "Candidatures":
        set_page("recruiter_applications")
        st.rerun()
    elif selected == "Chatbot HiRo":
        set_page("recruiter_chatbot")
        st.rerun()
    
    # Titre de la page
    st.markdown("<h1 style='color: #00A8A8;'>Gestion des fiches de poste</h1>", unsafe_allow_html=True)
    
    # Bouton pour créer une nouvelle fiche
    col1, col2 = st.columns([4, 1])
    with col2:
        if st.button("➕ Créer une fiche", key="create_job_btn"):
            set_page("recruiter_chatbot")  # Rediriger vers le chatbot pour création
            st.rerun()
    
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
            status = st.selectbox(
                "Statut", 
                ["Tous", "Actif", "En pause", "Clôturé"]
            )
        
        # Recherche par mots-clés
        search_query = st.text_input("Recherche par mots-clés", placeholder="Développeur, Python, Data...")
    
    # Récupération des fiches de poste
    try:
        # Appel à l'API pour récupérer les fiches de poste
        response = get_job_postings()
        
        if isinstance(response, dict) and "error" in response:
            st.error(f"Erreur lors de la récupération des fiches: {response['error']}")
            jobs = []
        else:
            jobs = response if isinstance(response, list) else []
        
        # Filtrage des fiches selon les critères sélectionnés
        filtered_jobs = []
        for job in jobs:
            # Filtrer par secteur
            if secteur != "Tous" and job.get("secteur") != secteur:
                continue
            
            # Filtrer par type de contrat
            if contrat != "Tous" and job.get("contrat") != contrat:
                continue
            
            # Filtrer par statut (à implémenter lorsque disponible dans les données)
            # if status != "Tous" and job.get("status") != status:
            #     continue
            
            # Filtrer par recherche textuelle
            if search_query and not (
                search_query.lower() in job.get("titre", "").lower() or
                search_query.lower() in job.get("content", "").lower() or
                any(search_query.lower() in comp.lower() for comp in job.get("competences", []))
            ):
                continue
            
            filtered_jobs.append(job)
        
        # Affichage des résultats
        st.markdown(f"<h3>{len(filtered_jobs)} fiche(s) de poste trouvée(s)</h3>", unsafe_allow_html=True)
        
        if not filtered_jobs:
            st.info("Aucune fiche ne correspond à vos critères de recherche.")
            
            # Bouton pour créer une nouvelle fiche
            if st.button("Créer une nouvelle fiche de poste"):
                set_page("recruiter_chatbot")
                st.rerun()
        else:
            for index, job in enumerate(filtered_jobs):
                with st.container():
                    st.markdown(f"""
                    <div style="background-color: #1E1E1E; border-radius: 10px; padding: 15px; margin-bottom: 15px; border: 1px solid #333333;">
                        <h3 style="color: #00A8A8; margin-top: 0;">{job.get('titre', 'Poste inconnu')}</h3>
                        <div style="display: flex; justify-content: space-between;">
                            <div>
                                <p><strong>Secteur:</strong> {job.get('secteur', 'Non spécifié')} | <strong>Contrat:</strong> {job.get('contrat', 'Non spécifié')}</p>
                                <p><strong>Niveau:</strong> {job.get('niveau', 'Non spécifié')}</p>
                                <p><strong>Compétences:</strong> {', '.join(job.get('competences', [])) if isinstance(job.get('competences', []), list) else job.get('competences', '')}</p>
                            </div>
                            <div style="text-align: center; background-color: #2A2A2A; padding: 8px 12px; border-radius: 16px; height: fit-content;">
                                <span>Actif</span>
                            </div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                
                    col1, col2, col3, col4 = st.columns([2, 2, 2, 1])
                    
                    with col1:
                        if st.button("👁️ Voir détails", key=f"view_{job.get('id', index)}"):
                            st.session_state.selected_job = job
                            set_page("recruiter_job_details")
                            st.rerun()
                    
                    with col2:
                        if st.button("👥 Voir candidats", key=f"candidates_{job.get('id', index)}"):
                            st.session_state.selected_job = job
                            set_page("recruiter_job_applications")
                            st.rerun()
                    
                    with col3:
                        # Téléchargement du PDF si disponible
                        if "fichierPDF" in job and job["fichierPDF"]:
                            try:
                                pdf_bytes = base64.b64decode(job["fichierPDF"])
                                st.download_button(
                                    label="📄 Télécharger PDF",
                                    data=pdf_bytes,
                                    file_name=f"{job.get('titre', 'fiche_poste')}.pdf",
                                    mime="application/pdf",
                                    key=f"pdf_{job.get('id', index)}"
                                )
                            except Exception as e:
                                st.error(f"Erreur PDF: {e}")
                        else:
                            st.markdown("<div style='height: 38px;'></div>", unsafe_allow_html=True)
                    
                    with col4:
                        if st.button("🗑️", key=f"delete_{job.get('id', index)}"):
                            # Ici, il faudrait implémenter la logique de suppression
                            # Pour l'instant, on affiche juste un message
                            st.warning(f"Fonctionnalité de suppression non implémentée")
                    
                    st.markdown("<hr>", unsafe_allow_html=True)
        
    except Exception as e:
        st.error(f"Une erreur s'est produite : {str(e)}")

def render_job_details():
    """Affiche les détails d'une fiche de poste pour les recruteurs"""
    if "user" not in st.session_state or not st.session_state.user:
        set_page("login")
        st.rerun()
        return
    
    if "selected_job" not in st.session_state or not st.session_state.selected_job:
        set_page("recruiter_job_postings")
        st.rerun()
        return
    
    job = st.session_state.selected_job
    
    render_top_bar()
    
    # Bouton de retour
    if st.button("← Retour aux fiches de poste"):
        set_page("recruiter_job_postings")
        st.rerun()
    
    # Affichage des détails de l'offre
    st.markdown(f"<h1 style='color: #00A8A8;'>{job.get('titre', 'Poste inconnu')}</h1>", unsafe_allow_html=True)
    
    # Actions
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📋 Modifier la fiche"):
            # Rediriger vers l'édition (à implémenter)
            st.warning("Fonctionnalité d'édition non implémentée")
    
    with col2:
        if st.button("👥 Voir les candidats"):
            set_page("recruiter_job_applications")
            st.rerun()
    
    with col3:
        # Téléchargement du PDF si disponible
        if "fichierPDF" in job and job["fichierPDF"]:
            try:
                pdf_bytes = base64.b64decode(job["fichierPDF"])
                st.download_button(
                    label="📄 Télécharger en PDF",
                    data=pdf_bytes,
                    file_name=f"{job.get('titre', 'fiche_poste')}.pdf",
                    mime="application/pdf"
                )
            except Exception as e:
                st.error(f"Erreur lors de la génération du PDF: {e}")
    
    # Infos principales
    st.markdown("<hr>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"**Secteur:** {job.get('secteur', 'Non spécifié')}")
    with col2:
        st.markdown(f"**Type de contrat:** {job.get('contrat', 'Non spécifié')}")
    with col3:
        st.markdown(f"**Niveau d'expérience:** {job.get('niveau', 'Non spécifié')}")
    
    # Compétences requises
    st.markdown("### Compétences requises")
    competences = job.get("competences", [])
    if isinstance(competences, str):
        competences = [comp.strip() for comp in competences.split(",")]
    
    if competences:
        cols = st.columns(min(5, len(competences)))
        for i, comp in enumerate(competences):
            with cols[i % len(cols)]:
                st.markdown(f"""
                <div style='background-color: #004D40; padding: 8px 12px; 
                     border-radius: 16px; margin: 4px; display: inline-block;'>
                    {comp}
                </div>
                """, unsafe_allow_html=True)
    else:
        st.info("Aucune compétence spécifiée")
    
    # Description du poste
    st.markdown("### Description du poste")
    st.markdown(job.get("content", "Aucune description disponible"))
    
    # Statistiques de la fiche de poste
    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("### Statistiques")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="stat-card">
            <div class="stat-label">Vues</div>
            <div class="stat-value">48</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="stat-card">
            <div class="stat-label">Candidatures</div>
            <div class="stat-value">5</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="stat-card">
            <div class="stat-label">Match moyen</div>
            <div class="stat-value">76%</div>
        </div>
        """, unsafe_allow_html=True)

if __name__ == "__main__":
    render_job_management()