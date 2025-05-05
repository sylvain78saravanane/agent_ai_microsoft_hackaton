import streamlit as st
import base64
import time
from streamlit_option_menu import option_menu
from utils.session_manager import set_page
from utils.api import generate_fiche_api
from views.components import render_top_bar, render_success_message, render_error_message

def render_chatbot():
    """Affiche l'interface du chatbot HiRo pour les recruteurs"""
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
        default_index=3,
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
    elif selected == "Candidatures":
        set_page("recruiter_applications")
        st.rerun()
    
    # Titre de la page
    st.markdown("<h1 style='color: #00A8A8;'>HiRo - Assistant RH Intelligent</h1>", unsafe_allow_html=True)
    
    # Initialisation de l'historique des messages
    if "chatbot_messages" not in st.session_state:
        st.session_state.chatbot_messages = [
            {
                "role": "assistant", 
                "content": "Bonjour! Je suis HiRo, votre assistant intelligent pour le recrutement. Comment puis-je vous aider aujourd'hui?"
            }
        ]
    
    if "fiche_inputs" not in st.session_state:
        st.session_state.fiche_inputs = {
            "titre": "",
            "secteur": "",
            "contrat": "",
            "niveau": "",
            "competences": ""
        }
    
    # Mode de conversation
    modes = ["Chat général", "Générer une fiche de poste", "Analyser des CV", "Comparer CV et fiche"]
    
    if "chatbot_mode" not in st.session_state:
        st.session_state.chatbot_mode = modes[0]
    
    # Sélection du mode
    selected_mode = st.selectbox(
        "Mode de conversation",
        modes,
        index=modes.index(st.session_state.chatbot_mode)
    )
    
    # Mise à jour du mode si changé
    if selected_mode != st.session_state.chatbot_mode:
        st.session_state.chatbot_mode = selected_mode
        
        # Message de changement de mode
        st.session_state.chatbot_messages.append({
            "role": "assistant",
            "content": f"Mode changé pour : {selected_mode}. Comment puis-je vous aider?"
        })
    
    # Affichage de l'historique de conversation
    st.markdown("""
    <div style="background-color: #121212; border-radius: 10px; padding: 20px; margin-bottom: 20px; border: 1px solid #333333; max-height: 400px; overflow-y: auto;">
    """, unsafe_allow_html=True)
    
    for msg in st.session_state.chatbot_messages:
        if msg["role"] == "user":
            st.markdown(f"""
            <div style="background-color: #2A2A2A; padding: 10px 15px; border-radius: 15px 15px 0 15px; margin: 10px 0; margin-left: 20%; margin-right: 5%; text-align: right;">
                {msg["content"]}
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div style="background-color: #004D40; padding: 10px 15px; border-radius: 15px 15px 15px 0; margin: 10px 0; margin-right: 20%; margin-left: 5%;">
                {msg["content"]}
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("""</div>""", unsafe_allow_html=True)
    
    # Interface spécifique au mode sélectionné
    if st.session_state.chatbot_mode == "Générer une fiche de poste":
        _render_job_generation_interface()
    elif st.session_state.chatbot_mode == "Analyser des CV":
        _render_cv_analysis_interface()
    elif st.session_state.chatbot_mode == "Comparer CV et fiche":
        _render_matching_interface()
    else:  # Chat général
        _render_general_chat_interface()

def _render_general_chat_interface():
    """Interface de chat général"""
    # Champ de saisie pour le message
    user_message = st.text_input("Votre message", placeholder="Posez une question à HiRo...")
    
    # Bouton d'envoi
    col1, col2 = st.columns([4, 1])
    with col2:
        send_button = st.button("Envoyer", use_container_width=True)
    
    # Traitement du message
    if send_button and user_message:
        # Ajouter le message de l'utilisateur à l'historique
        st.session_state.chatbot_messages.append({
            "role": "user",
            "content": user_message
        })
        
        # Simuler une réponse de l'assistant (à remplacer par un appel à l'API)
        with st.spinner("HiRo réfléchit..."):
            time.sleep(1)  # Simuler le temps de traitement
            
            # Réponses prédéfinies selon le contenu du message (à remplacer par l'IA)
            if "fiche" in user_message.lower() or "poste" in user_message.lower():
                response = "Je peux vous aider à générer une fiche de poste. Veuillez passer en mode 'Générer une fiche de poste' pour commencer."
            elif "cv" in user_message.lower() or "candidat" in user_message.lower():
                response = "Je peux analyser des CV ou les comparer à vos fiches de poste. Sélectionnez le mode correspondant pour commencer."
            elif "bonjour" in user_message.lower() or "salut" in user_message.lower():
                response = f"Bonjour {st.session_state.user.get('prenom', '')}! Comment puis-je vous aider aujourd'hui?"
            else:
                response = "Je suis HiRo, votre assistant RH. Je peux vous aider à générer des fiches de poste, analyser des CV, ou effectuer des correspondances entre CV et fiches de poste. Sélectionnez le mode qui vous intéresse pour commencer."
            
            # Ajouter la réponse à l'historique
            st.session_state.chatbot_messages.append({
                "role": "assistant",
                "content": response
            })
        
        # Rafraîchir pour afficher les nouveaux messages
        st.rerun()


def _render_job_generation_interface():
    """Interface pour la génération de fiches de poste"""
    # Utilisation de colonnes pour le titre
    st.subheader("Générer une fiche de poste")
    
    # Remplacer st.form par des champs normaux
    col1, col2 = st.columns(2)
    
    with col1:
        titre = st.text_input("Titre du poste", value=st.session_state.fiche_inputs.get("titre", ""))
        secteur = st.text_input("Secteur", value=st.session_state.fiche_inputs.get("secteur", ""))
    
    with col2:
        contrat = st.selectbox("Type de contrat", 
                             ["CDI", "CDD", "Stage", "Alternance", "Freelance"],
                             index=0 if not st.session_state.fiche_inputs.get("contrat") else 
                             ["CDI", "CDD", "Stage", "Alternance", "Freelance"].index(st.session_state.fiche_inputs.get("contrat")))
        niveau = st.text_input("Niveau d'expérience requis", value=st.session_state.fiche_inputs.get("niveau", ""))
    
    competences = st.text_area("Compétences clés (séparées par des virgules)", 
                              value=st.session_state.fiche_inputs.get("competences", ""))
    
    # Bouton de génération en dehors du formulaire
    submitted = st.button("Générer la fiche de poste")
    
    if submitted:
        if not titre or not secteur or not contrat or not niveau or not competences:
            st.error("Veuillez remplir tous les champs.")
        else:
            # Sauvegarder les inputs
            st.session_state.fiche_inputs = {
                "titre": titre,
                "secteur": secteur,
                "contrat": contrat,
                "niveau": niveau,
                "competences": competences
            }
            
            # Appel à l'API de génération de fiche
            with st.spinner("Génération de la fiche en cours..."):
                    try:
                        response = generate_fiche_api(
                            titre=titre,
                            secteur=secteur,
                            contrat=contrat,
                            niveau=niveau,
                            competences=competences
                        )
                        
                        if isinstance(response, dict) and "error" in response:
                            st.error(f"Erreur lors de la génération: {response['error']}")
                        elif isinstance(response, str) and "Erreur" in response:
                            st.error(response)
                        else:
                            # Ajouter les messages à l'historique
                            st.session_state.chatbot_messages.append({
                                "role": "user",
                                "content": f"Générer une fiche de poste pour {titre} ({secteur}, {contrat})"
                            })
                            
                            fiche_content = response.get("fiche", "") if isinstance(response, dict) else str(response)
                            
                            st.session_state.chatbot_messages.append({
                                "role": "assistant",
                                "content": f"J'ai généré une fiche de poste pour {titre}. Voici le résultat :"
                            })
                            
                            # Afficher la fiche générée
                            st.markdown("""
                            <div style="background-color: #1E1E1E; border-radius: 10px; padding: 20px; margin: 20px 0; border: 1px solid #333333;">
                            """, unsafe_allow_html=True)
                            
                            st.markdown(fiche_content)
                            
                            st.markdown("""</div>""", unsafe_allow_html=True)
                            
                            # Bouton de téléchargement si PDF disponible
                            if isinstance(response, dict) and "fichierPDF" in response:
                                try:
                                    pdf_bytes = base64.b64decode(response["fichierPDF"])
                                    st.download_button(
                                        label="📄 Télécharger en PDF",
                                        data=pdf_bytes,
                                        file_name=f"{titre}_fiche_poste.pdf",
                                        mime="application/pdf"
                                    )
                                except Exception as e:
                                    st.error(f"Erreur lors de la génération du PDF: {e}")
                            
                            # Option pour sauvegarder la fiche
                            save_col1, save_col2 = st.columns(2)
                            
                            with save_col1:
                                if st.button("💾 Sauvegarder cette fiche"):
                                    render_success_message("Fiche de poste sauvegardée avec succès!")
                            
                            with save_col2:
                                if st.button("🔄 Générer une nouvelle fiche"):
                                    # Réinitialiser les champs
                                    st.session_state.fiche_inputs = {
                                        "titre": "",
                                        "secteur": "",
                                        "contrat": "",
                                        "niveau": "",
                                        "competences": ""
                                    }
                                    st.rerun()
                    
                    except Exception as e:
                        st.error(f"Erreur lors de la génération: {str(e)}")

def _render_cv_analysis_interface():
    """Interface pour l'analyse de CV"""
    st.subheader("Analyser un CV")
    
    # Uploader un CV
    cv_file = st.file_uploader("Télécharger un CV à analyser", type=["pdf", "docx"])
    
    if cv_file:
        st.markdown(f"Fichier sélectionné: **{cv_file.name}**")
        
        # Bouton d'analyse
        if st.button("Analyser ce CV"):
            # Simuler l'analyse (à remplacer par un appel à l'API)
            with st.spinner("Analyse du CV en cours..."):
                time.sleep(2)  # Simuler le temps d'analyse
                
                # Ajouter les messages à l'historique
                st.session_state.chatbot_messages.append({
                    "role": "user",
                    "content": f"Analyser le CV {cv_file.name}"
                })
                
                st.session_state.chatbot_messages.append({
                    "role": "assistant",
                    "content": f"J'ai analysé le CV {cv_file.name}. Voici mon évaluation :"
                })
                
                # Afficher l'analyse fictive
                st.markdown("""
                <div style="background-color: #1E1E1E; border-radius: 10px; padding: 20px; margin: 20px 0; border: 1px solid #333333;">
                    <h3 style="color: #00A8A8;">Analyse du CV</h3>
                    
                    <p><strong>Profil général:</strong> Candidat avec 5 ans d'expérience en développement web</p>
                    
                    <p><strong>Compétences identifiées:</strong></p>
                    <div style="display: flex; flex-wrap: wrap; margin-bottom: 15px;">
                        <div style="background-color: #004D40; padding: 5px 10px; border-radius: 15px; margin: 5px;">JavaScript</div>
                        <div style="background-color: #004D40; padding: 5px 10px; border-radius: 15px; margin: 5px;">React</div>
                        <div style="background-color: #004D40; padding: 5px 10px; border-radius: 15px; margin: 5px;">Node.js</div>
                        <div style="background-color: #004D40; padding: 5px 10px; border-radius: 15px; margin: 5px;">SQL</div>
                        <div style="background-color: #004D40; padding: 5px 10px; border-radius: 15px; margin: 5px;">Git</div>
                    </div>
                    
                    <p><strong>Forces:</strong> Expérience significative en développement frontend, bonne connaissance des frameworks modernes</p>
                    
                    <p><strong>Points d'amélioration:</strong> Peu d'expérience en management d'équipe, connaissances en backend à approfondir</p>
                    
                    <p><strong>Recommandation:</strong> Ce profil conviendrait pour un poste de Développeur Frontend Senior ou de Lead Developer dans une équipe technique.</p>
                </div>
                """, unsafe_allow_html=True)
                
                # Options post-analyse
                col1, col2 = st.columns(2)
                
                with col1:
                    if st.button("Rechercher des postes correspondants"):
                        st.session_state.chatbot_messages.append({
                            "role": "user",
                            "content": "Rechercher des postes correspondants à ce CV"
                        })
                        
                        st.session_state.chatbot_messages.append({
                            "role": "assistant",
                            "content": "Voici les postes qui pourraient correspondre à ce profil :\n- Développeur Frontend Senior\n- Lead Developer React\n- Architecte Frontend"
                        })
                        
                        st.rerun()
                
                with col2:
                    if st.button("Analyser un autre CV"):
                        # Réinitialiser l'uploader
                        st.rerun()

def _render_matching_interface():
    """Interface pour la comparaison CV / fiche de poste"""
    st.subheader("Comparer un CV avec une fiche de poste")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### CV")
        cv_file = st.file_uploader("Télécharger un CV", type=["pdf", "docx"])
    
    with col2:
        st.markdown("### Fiche de poste")
        # Option pour sélectionner une fiche existante ou en uploader une
        fiche_option = st.radio("Choisir une fiche de poste", ["Sélectionner parmi les fiches existantes", "Télécharger une nouvelle fiche"])
        
        if fiche_option == "Sélectionner parmi les fiches existantes":
            fiche_id = st.selectbox("Fiche de poste", ["Développeur Frontend React", "Data Scientist Senior", "Chef de Projet IT", "Architecte Cloud"])
        else:
            fiche_file = st.file_uploader("Télécharger une fiche de poste", type=["pdf", "docx"])
    
    # Bouton de comparaison
    if st.button("Comparer"):
        if cv_file and (fiche_option == "Sélectionner parmi les fiches existantes" or (fiche_option == "Télécharger une nouvelle fiche" and 'fiche_file' in locals() and fiche_file)):
            # Simuler la comparaison (à remplacer par un appel à l'API)
            with st.spinner("Comparaison en cours..."):
                time.sleep(2)  # Simuler le temps de traitement
                
                # Ajouter les messages à l'historique
                fiche_name = fiche_id if fiche_option == "Sélectionner parmi les fiches existantes" else fiche_file.name
                
                st.session_state.chatbot_messages.append({
                    "role": "user",
                    "content": f"Comparer le CV {cv_file.name} avec la fiche de poste {fiche_name}"
                })
                
                st.session_state.chatbot_messages.append({
                    "role": "assistant",
                    "content": f"J'ai comparé le CV {cv_file.name} avec la fiche de poste {fiche_name}. Voici les résultats :"
                })
                
                # Afficher le résultat fictif de la comparaison
                match_score = 85  # Score fictif
                
                st.markdown(f"""
                <div style="background-color: #1E1E1E; border-radius: 10px; padding: 20px; margin: 20px 0; border: 1px solid #333333;">
                    <h3 style="color: #00A8A8;">Résultat de la comparaison</h3>
                    
                    <div style="text-align: center; margin: 20px 0;">
                        <div style="font-size: 60px; font-weight: bold; color: {'#00BFA5' if match_score >= 80 else '#FFAB40'};">
                            {match_score}%
                        </div>
                        <p>Score de compatibilité</p>
                    </div>
                    
                    <h4 style="color: #00A8A8;">Points forts du candidat</h4>
                    <p>Le candidat possède une solide expérience en développement frontend avec React, ainsi qu'une bonne maîtrise des technologies web modernes. Ses compétences en JavaScript et en intégration d'API correspondent parfaitement aux exigences du poste.</p>
                    
                    <h4 style="color: #00A8A8;">Écarts identifiés</h4>
                    <p>Le candidat manque d'expérience en gestion de projets agiles et en tests automatisés, deux compétences mentionnées dans la fiche de poste. Une formation complémentaire pourrait être envisagée dans ces domaines.</p>
                    
                    <h4 style="color: #00A8A8;">Recommandation</h4>
                    <p>Ce candidat présente un bon profil pour le poste, avec une compatibilité élevée sur les compétences techniques essentielles. Nous recommandons de poursuivre le processus de recrutement et de planifier un entretien technique.</p>
                </div>
                """, unsafe_allow_html=True)
                
                # Options post-comparaison
                col1, col2 = st.columns(2)
                
                with col1:
                    if st.button("Planifier un entretien"):
                        st.session_state.chatbot_messages.append({
                            "role": "user",
                            "content": "Planifier un entretien avec ce candidat"
                        })
                        
                        st.session_state.chatbot_messages.append({
                            "role": "assistant",
                            "content": "Pour planifier un entretien, veuillez accéder à la section Candidatures et sélectionner ce candidat."
                        })
                        
                        st.rerun()
                
                with col2:
                    if st.button("Comparer avec d'autres postes"):
                        st.session_state.chatbot_messages.append({
                            "role": "user",
                            "content": "Comparer ce CV avec d'autres postes"
                        })
                        
                        st.session_state.chatbot_messages.append({
                            "role": "assistant",
                            "content": "Je vais comparer ce CV avec nos autres fiches de poste. Cette fonctionnalité sera bientôt disponible."
                        })
                        
                        st.rerun()
        
        else:
            st.error("Veuillez fournir à la fois un CV et une fiche de poste pour effectuer la comparaison.")

if __name__ == "__main__":
    render_chatbot()