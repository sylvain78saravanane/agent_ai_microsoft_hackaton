import streamlit as st
from streamlit_option_menu import option_menu
from utils.session_manager import set_page
from views.components import render_top_bar, render_candidate_card

def render_candidate_management():
    """Affiche la gestion des candidatures pour les recruteurs"""
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
    if selected == "Tableau de bord":
        set_page("recruiter_dashboard")
        st.rerun()
    elif selected == "Fiches de poste":
        set_page("recruiter_job_postings")
        st.rerun()
    elif selected == "Chatbot HiRo":
        set_page("recruiter_chatbot")
        st.rerun()
    
    # Titre de la page
    st.markdown("<h1 style='color: #00A8A8;'>Gestion des candidatures</h1>", unsafe_allow_html=True)
    
    # Filtres de recherche
    with st.expander("Filtres de recherche", expanded=True):
        col1, col2, col3 = st.columns(3)
        
        with col1:
            poste = st.selectbox(
                "Poste", 
                ["Tous", "Data Scientist Senior", "Développeur Frontend React", "Chef de Projet IT", "Architecte Cloud"]
            )
        
        with col2:
            statut = st.selectbox(
                "Statut", 
                ["Tous", "Nouveau", "Analysé", "Entretien", "Retenu", "Rejeté"]
            )
        
        with col3:
            matching = st.select_slider(
                "Score de matching minimum", 
                options=[0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100],
                value=0
            )
        
        # Recherche par nom
        search_query = st.text_input("Recherche par nom", placeholder="Nom du candidat...")
    
    # Candidatures fictives pour la démo
    applications = [
        {
            "id": "app_001",
            "nom": "Dupont",
            "prenom": "Marie",
            "email": "m.dupont@email.com",
            "poste": "Data Scientist Senior",
            "date": "05/05/2025",
            "status": "Nouveau",
            "matching": 92,
            "competences": ["Python", "Machine Learning", "SQL", "Data Visualization", "Deep Learning"]
        },
        {
            "id": "app_002",
            "nom": "Martin",
            "prenom": "Thomas",
            "email": "t.martin@email.com",
            "poste": "Développeur Frontend React",
            "date": "04/05/2025",
            "status": "Entretien",
            "matching": 85,
            "competences": ["React", "JavaScript", "HTML/CSS", "TypeScript", "Redux"]
        },
        {
            "id": "app_003",
            "nom": "Lefebvre",
            "prenom": "Julie",
            "email": "j.lefebvre@email.com",
            "poste": "Chef de Projet IT",
            "date": "02/05/2025",
            "status": "Analysé",
            "matching": 78,
            "competences": ["Gestion de projet", "Agile", "JIRA", "Planification", "MS Project"]
        },
        {
            "id": "app_004",
            "nom": "Dubois",
            "prenom": "Pierre",
            "email": "p.dubois@email.com",
            "poste": "Architecte Cloud",
            "date": "01/05/2025",
            "status": "Rejeté",
            "matching": 65,
            "competences": ["AWS", "Azure", "Docker", "Kubernetes", "Infrastructure as Code"]
        }
    ]
    
    # Filtrage des candidatures selon les critères sélectionnés
    filtered_applications = []
    for app in applications:
        # Filtrer par poste
        if poste != "Tous" and app["poste"] != poste:
            continue
        
        # Filtrer par statut
        if statut != "Tous" and app["status"] != statut:
            continue
        
        # Filtrer par score de matching
        if app["matching"] < matching:
            continue
        
        # Filtrer par recherche textuelle
        if search_query and not (
            search_query.lower() in app["nom"].lower() or
            search_query.lower() in app["prenom"].lower() or
            search_query.lower() in app["email"].lower()
        ):
            continue
        
        filtered_applications.append(app)
    
    # Affichage des résultats
    st.markdown(f"<h3>{len(filtered_applications)} candidature(s) trouvée(s)</h3>", unsafe_allow_html=True)
    
    if not filtered_applications:
        st.info("Aucune candidature ne correspond à vos critères de recherche.")
    else:
        for app in filtered_applications:
            with st.container():
                st.markdown(f"""
                <div style="background-color: #1E1E1E; border-radius: 10px; padding: 15px; margin-bottom: 15px; border: 1px solid #333333;">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <div>
                            <h3 style="color: #00A8A8; margin-top: 0;">{app['prenom']} {app['nom']}</h3>
                            <p><strong>Poste:</strong> {app['poste']}</p>
                            <p><strong>Date:</strong> {app['date']} | <strong>Statut:</strong> 
                                <span style="background-color: {
                                    '#004D40' if app['status'] == 'Entretien' else 
                                    '#2A2A2A' if app['status'] == 'Nouveau' else 
                                    '#4A1212' if app['status'] == 'Rejeté' else '#2A2A2A'
                                }; padding: 4px 10px; border-radius: 10px;">
                                    {app['status']}
                                </span>
                            </p>
                            <p><strong>Compétences:</strong> {', '.join(app['competences'])}</p>
                        </div>
                        <div style="text-align: center; padding: 10px; background-color: {'#004D40' if app['matching'] >= 80 else '#2A2A2A'}; border-radius: 50%; width: 60px; height: 60px; display: flex; align-items: center; justify-content: center;">
                            <span style="font-size: 20px; font-weight: bold; color: {'#00BFA5' if app['matching'] >= 80 else '#FFAB40'};">
                                {app['matching']}%
                            </span>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                col1, col2, col3, col4 = st.columns([2, 2, 2, 1])
                
                with col1:
                    if st.button("👁️ Voir CV", key=f"view_cv_{app['id']}"):
                        st.session_state.selected_candidate = app
                        set_page("recruiter_candidate_details")
                        st.rerun()
                
                with col2:
                    if st.button("📋 Changer statut", key=f"status_{app['id']}"):
                        # Ici, il faudrait implémenter la logique de changement de statut
                        # Pour l'instant, on affiche juste un message
                        st.warning("Fonctionnalité de changement de statut à implémenter")
                
                with col3:
                    if st.button("📊 Analyse IA", key=f"ai_{app['id']}"):
                        st.session_state.selected_candidate = app
                        set_page("recruiter_candidate_analysis")
                        st.rerun()
                
                with col4:
                    if st.button("✉️", key=f"email_{app['id']}"):
                        # Ici, il faudrait implémenter la logique d'envoi d'email
                        # Pour l'instant, on affiche juste un message
                        st.warning("Fonctionnalité d'envoi d'email à implémenter")
    
    # Ajout d'une section pour les candidatures par poste
    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("<h2>Répartition des candidatures par poste</h2>", unsafe_allow_html=True)
    
    # Compter les candidatures par poste
    postes = {}
    for app in applications:
        if app["poste"] in postes:
            postes[app["poste"]] += 1
        else:
            postes[app["poste"]] = 1
    
    # Afficher les résultats sous forme de graphique simplifié
    for poste, count in postes.items():
        st.markdown(f"""
        <div style="margin-bottom: 10px;">
            <p style="margin-bottom: 5px;"><strong>{poste}</strong></p>
            <div style="background-color: #004D40; width: {count*10}%; height: 20px; border-radius: 10px;">
                <div style="padding-left: 10px; line-height: 20px; color: white;">{count}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

def render_candidate_details():
    """Affiche les détails d'un candidat pour les recruteurs"""
    if "user" not in st.session_state or not st.session_state.user:
        set_page("login")
        st.rerun()
        return
    
    if "selected_candidate" not in st.session_state or not st.session_state.selected_candidate:
        set_page("recruiter_applications")
        st.rerun()
        return
    
    candidate = st.session_state.selected_candidate
    
    render_top_bar()
    
    # Bouton de retour
    if st.button("← Retour aux candidatures"):
        set_page("recruiter_applications")
        st.rerun()
    
    # Affichage des détails du candidat
    st.markdown(f"<h1 style='color: #00A8A8;'>{candidate['prenom']} {candidate['nom']}</h1>", unsafe_allow_html=True)
    
    # Actions rapides
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📊 Analyser avec HiRo"):
            set_page("recruiter_candidate_analysis")
            st.rerun()
    
    with col2:
        if st.button("✉️ Contacter"):
            # Ici, il faudrait implémenter la logique d'envoi d'email
            # Pour l'instant, on affiche juste un message
            st.warning("Fonctionnalité d'envoi d'email à implémenter")
    
    with col3:
        if st.button("📋 Changer statut"):
            # Ici, il faudrait implémenter la logique de changement de statut
            # Pour l'instant, on affiche juste un message
            st.warning("Fonctionnalité de changement de statut à implémenter")
    
    # Informations principales
    st.markdown("<hr>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"""
        <div style="background-color: #1E1E1E; border-radius: 10px; padding: 15px; margin-bottom: 15px; border: 1px solid #333333;">
            <h3 style="color: #00A8A8; margin-top: 0;">Informations personnelles</h3>
            <p><strong>Email:</strong> {candidate['email']}</p>
            <p><strong>Statut actuel:</strong> {candidate['status']}</p>
            <p><strong>Candidature le:</strong> {candidate['date']}</p>
            <p><strong>Poste:</strong> {candidate['poste']}</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div style="background-color: #1E1E1E; border-radius: 10px; padding: 15px; margin-bottom: 15px; border: 1px solid #333333;">
            <h3 style="color: #00A8A8; margin-top: 0;">Compétences</h3>
            <div style="display: flex; flex-wrap: wrap;">
                {' '.join([f'<div style="background-color: #004D40; padding: 5px 10px; border-radius: 15px; margin: 5px;">{comp}</div>' for comp in candidate['competences']])}
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div style="background-color: #1E1E1E; border-radius: 10px; padding: 15px; margin-bottom: 15px; border: 1px solid #333333;">
            <h3 style="color: #00A8A8; margin-top: 0;">Score de matching</h3>
            <div style="text-align: center; padding: 20px;">
                <div style="font-size: 60px; font-weight: bold; color: {'#00BFA5' if candidate['matching'] >= 80 else '#FFAB40'};">
                    {candidate['matching']}%
                </div>
                <p>Adéquation avec le poste de {candidate['poste']}</p>
            </div>
        </div>
        
        <div style="background-color: #1E1E1E; border-radius: 10px; padding: 15px; margin-bottom: 15px; border: 1px solid #333333;">
            <h3 style="color: #00A8A8; margin-top: 0;">Historique</h3>
            <ul style="list-style-type: none; padding-left: 0;">
                <li style="padding: 8px 0; border-bottom: 1px solid #333333;">
                    <span style="color: #AAAAAA;">05/05/2025</span> - CV reçu
                </li>
                <li style="padding: 8px 0; border-bottom: 1px solid #333333;">
                    <span style="color: #AAAAAA;">05/05/2025</span> - Analyse IA effectuée
                </li>
                <li style="padding: 8px 0;">
                    <span style="color: #AAAAAA;">06/05/2025</span> - Changement de statut à "{candidate['status']}"
                </li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    # CV du candidat (fictif pour la démo)
    st.markdown("<h2>CV du candidat</h2>", unsafe_allow_html=True)
    
    # Ici, on simule l'affichage d'un CV
    st.markdown(f"""
    <div style="background-color: #1E1E1E; border-radius: 10px; padding: 20px; margin-bottom: 15px; border: 1px solid #333333;">
        <h2 style="text-align: center; color: #00A8A8;">{candidate['prenom']} {candidate['nom']}</h2>
        <p style="text-align: center;">{candidate['email']} | Paris, France</p>
        
        <h3 style="color: #00A8A8; border-bottom: 1px solid #333333; padding-bottom: 5px;">Expérience Professionnelle</h3>
        <p><strong>Senior {candidate['poste']}</strong> | Entreprise XYZ | 2022-2025</p>
        <ul>
            <li>Réalisation de projets complexes dans le domaine du {candidate['poste']}</li>
            <li>Management d'une équipe de 5 personnes</li>
            <li>Mise en place de méthodologies agiles</li>
        </ul>
        
        <p><strong>{candidate['poste']}</strong> | Entreprise ABC | 2018-2022</p>
        <ul>
            <li>Participation à des projets d'envergure internationale</li>
            <li>Développement de solutions innovantes</li>
            <li>Collaboration avec différentes équipes</li>
        </ul>
        
        <h3 style="color: #00A8A8; border-bottom: 1px solid #333333; padding-bottom: 5px;">Formation</h3>
        <p><strong>Master en Informatique</strong> | Université de Paris | 2018</p>
        <p><strong>Licence en Informatique</strong> | Université de Lyon | 2016</p>
        
        <h3 style="color: #00A8A8; border-bottom: 1px solid #333333; padding-bottom: 5px;">Compétences</h3>
        <div style="display: flex; flex-wrap: wrap;">
            {' '.join([f'<div style="background-color: #004D40; padding: 5px 10px; border-radius: 15px; margin: 5px;">{comp}</div>' for comp in candidate['competences']])}
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Bouton pour analyser le CV avec HiRo
    if st.button("Analyser ce CV avec HiRo", use_container_width=True):
        set_page("recruiter_candidate_analysis")
        st.rerun()

def render_candidate_analysis():
    """Affiche l'analyse IA d'un candidat pour les recruteurs"""
    if "user" not in st.session_state or not st.session_state.user:
        set_page("login")
        st.rerun()
        return
    
    if "selected_candidate" not in st.session_state or not st.session_state.selected_candidate:
        set_page("recruiter_applications")
        st.rerun()
        return
    
    candidate = st.session_state.selected_candidate
    
    render_top_bar()
    
    # Bouton de retour
    if st.button("← Retour au profil"):
        set_page("recruiter_candidate_details")
        st.rerun()
    
    # Titre de la page
    st.markdown(f"<h1 style='color: #00A8A8;'>Analyse IA - {candidate['prenom']} {candidate['nom']}</h1>", unsafe_allow_html=True)
    
    # Affichage de l'analyse (fictive pour la démo)
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown(f"""
        <div style="background-color: #1E1E1E; border-radius: 10px; padding: 20px; margin-bottom: 15px; border: 1px solid #333333;">
            <h3 style="color: #00A8A8; margin-top: 0;">Synthèse de l'analyse</h3>
            <p>
                <strong>Score de matching:</strong> <span style="color: {'#00BFA5' if candidate['matching'] >= 80 else '#FFAB40'}; font-weight: bold;">{candidate['matching']}%</span>
            </p>
            <p>
                Ce candidat présente un profil <strong>très adapté</strong> au poste de {candidate['poste']}. 
                Ses compétences en {', '.join(candidate['competences'][:3])} correspondent parfaitement aux exigences du poste.
            </p>
            <p>
                <strong>Points forts:</strong> Excellente maîtrise technique, expérience significative dans le domaine, capacité à travailler en équipe.
            </p>
            <p>
                <strong>Points à approfondir:</strong> Expérience en gestion de projet, connaissance de l'environnement spécifique de l'entreprise.
            </p>
            <p>
                <strong>Recommandation:</strong> Ce candidat mérite de passer à l'étape d'entretien technique rapidement.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div style="background-color: #1E1E1E; border-radius: 10px; padding: 20px; margin-bottom: 15px; border: 1px solid #333333;">
            <h3 style="color: #00A8A8; margin-top: 0;">Analyse détaillée des compétences</h3>
            <table style="width: 100%;">
                <tr>
                    <th style="text-align: left; padding: 8px; border-bottom: 1px solid #333333;">Compétence</th>
                    <th style="text-align: center; padding: 8px; border-bottom: 1px solid #333333;">Niveau requis</th>
                    <th style="text-align: center; padding: 8px; border-bottom: 1px solid #333333;">Niveau estimé</th>
                    <th style="text-align: center; padding: 8px; border-bottom: 1px solid #333333;">Match</th>
                </tr>
        """, unsafe_allow_html=True)
        
        # Générer des données fictives pour chaque compétence
        for i, comp in enumerate(candidate['competences']):
            niveau_requis = 4  # Sur 5
            niveau_estime = min(5, max(3, (4 + (i % 3) - 1)))  # Entre 3 et 5
            match_percentage = int((niveau_estime / niveau_requis) * 100)
            
            st.markdown(f"""
                <tr>
                    <td style="padding: 8px; border-bottom: 1px solid #333333;">{comp}</td>
                    <td style="text-align: center; padding: 8px; border-bottom: 1px solid #333333;">{"●" * niveau_requis}{"○" * (5-niveau_requis)}</td>
                    <td style="text-align: center; padding: 8px; border-bottom: 1px solid #333333;">{"●" * niveau_estime}{"○" * (5-niveau_estime)}</td>
                    <td style="text-align: center; padding: 8px; border-bottom: 1px solid #333333; color: {'#00BFA5' if match_percentage >= 80 else '#FFAB40'};">
                        {match_percentage}%
                    </td>
                </tr>
            """, unsafe_allow_html=True)
        
        st.markdown("""
            </table>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div style="background-color: #1E1E1E; border-radius: 10px; padding: 20px; margin-bottom: 15px; border: 1px solid #333333;">
            <h3 style="color: #00A8A8; margin-top: 0;">Questions suggérées pour l'entretien</h3>
            <ol>
                <li>Pouvez-vous décrire un projet récent où vous avez utilisé {candidate['competences'][0]} ?</li>
                <li>Comment gérez-vous les situations de forte pression dans un contexte de projet ?</li>
                <li>Quelle est votre approche pour rester à jour concernant les nouvelles technologies dans votre domaine ?</li>
                <li>Comment collaborez-vous avec les autres départements ?</li>
                <li>Quelle est votre vision à long terme pour votre carrière dans le domaine de {candidate['poste']} ?</li>
            </ol>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div style="background-color: #1E1E1E; border-radius: 10px; padding: 20px; margin-bottom: 15px; border: 1px solid #333333;">
            <h3 style="color: #00A8A8; margin-top: 0;">Score global</h3>
            <div style="text-align: center; padding: 20px;">
                <div style="font-size: 70px; font-weight: bold; color: {'#00BFA5' if candidate['matching'] >= 80 else '#FFAB40'};">
                    {candidate['matching']}%
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div style="background-color: #1E1E1E; border-radius: 10px; padding: 20px; margin-bottom: 15px; border: 1px solid #333333;">
            <h3 style="color: #00A8A8; margin-top: 0;">Répartition des compétences</h3>
            <div style="margin-top: 15px;">
                <p><strong>Techniques:</strong></p>
                <div style="background-color: #2A2A2A; width: 100%; height: 10px; border-radius: 5px; margin-bottom: 15px;">
                    <div style="background-color: #00A8A8; width: 90%; height: 10px; border-radius: 5px;"></div>
                </div>
                
                <p><strong>Soft skills:</strong></p>
                <div style="background-color: #2A2A2A; width: 100%; height: 10px; border-radius: 5px; margin-bottom: 15px;">
                    <div style="background-color: #00A8A8; width: 75%; height: 10px; border-radius: 5px;"></div>
                </div>
                
                <p><strong>Expérience:</strong></p>
                <div style="background-color: #2A2A2A; width: 100%; height: 10px; border-radius: 5px; margin-bottom: 15px;">
                    <div style="background-color: #00A8A8; width: 85%; height: 10px; border-radius: 5px;"></div>
                </div>
                
                <p><strong>Formation:</strong></p>
                <div style="background-color: #2A2A2A; width: 100%; height: 10px; border-radius: 5px; margin-bottom: 15px;">
                    <div style="background-color: #00A8A8; width: 80%; height: 10px; border-radius: 5px;"></div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div style="background-color: #1E1E1E; border-radius: 10px; padding: 20px; margin-bottom: 15px; border: 1px solid #333333;">
            <h3 style="color: #00A8A8; margin-top: 0;">Actions recommandées</h3>
            <ul style="list-style-type: none; padding-left: 0;">
                <li style="padding: 8px 0; border-bottom: 1px solid #333333;">
                    ✅ Programmer un entretien technique
                </li>
                <li style="padding: 8px 0; border-bottom: 1px solid #333333;">
                    ✅ Vérifier les références professionnelles
                </li>
                <li style="padding: 8px 0;">
                    ✅ Préparer un test pratique sur {candidate['competences'][0]}
                </li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    # Boutons d'action
    st.markdown("<hr>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("💼 Changer le statut", use_container_width=True):
            st.warning("Fonctionnalité à implémenter")
    
    with col2:
        if st.button("📅 Planifier un entretien", use_container_width=True):
            st.warning("Fonctionnalité à implémenter")
    
    with col3:
        if st.button("✉️ Contacter le candidat", use_container_width=True):
            st.warning("Fonctionnalité à implémenter")

if __name__ == "__main__":
    render_candidate_management()