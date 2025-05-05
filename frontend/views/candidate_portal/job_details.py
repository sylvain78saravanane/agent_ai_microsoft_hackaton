import streamlit as st
import base64
from datetime import datetime
import tempfile
import os
import time
from utils.session_manager import set_page
from utils.api import add_cv
from utils.validators import validate_email, validate_phone
from views.components import render_top_bar

def render_job_details():
    """Affiche les détails d'une offre d'emploi et le formulaire de candidature"""
    if "user" not in st.session_state or not st.session_state.user:
        set_page("login")
        st.rerun()
        return
    
    if "selected_job" not in st.session_state or not st.session_state.selected_job:
        set_page("candidate_jobs")
        st.rerun()
        return
    
    job = st.session_state.selected_job
    
    render_top_bar()
    
    # Bouton de retour
    if st.button("← Retour aux offres"):
        set_page("candidate_jobs")
        st.rerun()
    
    # Affichage des détails de l'offre
    st.markdown(f"<h1 style='color: #00A8A8;'>{job.get('titre', 'Poste inconnu')}</h1>", unsafe_allow_html=True)
    
    # Infos principales
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
    
    # PDF de la fiche de poste
    if "fichierPDF" in job and job["fichierPDF"]:
        try:
            pdf_bytes = base64.b64decode(job["fichierPDF"])
            st.download_button(
                label="📄 Télécharger la fiche de poste en PDF",
                data=pdf_bytes,
                file_name=f"{job.get('titre', 'fiche_poste')}.pdf",
                mime="application/pdf"
            )
        except Exception as e:
            st.error(f"Erreur lors de la génération du PDF: {e}")
    
    # Formulaire de candidature
    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("## Candidater à cette offre", unsafe_allow_html=True)
    
    with st.form(key="candidature_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            nom = st.text_input("Nom*", value=st.session_state.user.get("nom", ""))
            email = st.text_input("Email*", value=st.session_state.user.get("userEmail", ""))
            telephone = st.text_input("Téléphone*")
        
        with col2:
            prenom = st.text_input("Prénom*", value=st.session_state.user.get("prenom", ""))
            adresse = st.text_input("Adresse (optionnel)")
            ville = st.text_input("Ville (optionnel)")
        
        # Formation et expérience
        st.subheader("Formation et expérience")
        formation = st.text_area("Formation", height=100, 
                                placeholder="Ex: Master en Informatique, Université de Paris (2020-2022)")
        experience = st.text_area("Expérience professionnelle", height=150,
                                 placeholder="Ex: Développeur Front-end chez ABC Corp (2022-2024)")
        
        # Compétences
        st.subheader("Compétences")
        competences_input = st.text_area("Vos compétences* (séparées par des virgules)", 
                                        help="Ex: Python, JavaScript, Gestion de projet...",
                                        placeholder="Python, React, Node.js...")
        
        # Informations complémentaires
        st.subheader("Informations complémentaires")
        col1, col2 = st.columns(2)
        with col1:
            disponibilite = st.date_input("Disponibilité")
            mobilite = st.selectbox("Mobilité", 
                                  ["Pas de mobilité", "Région", "France", "International"])
        with col2:
            pretentions = st.text_input("Prétentions salariales", 
                                       placeholder="Ex: 45-50K€")
            teletravail = st.selectbox("Télétravail", 
                                      ["Sur site uniquement", "Hybride", "Télétravail complet"])
        
        # CV et Lettre de motivation
        st.subheader("Documents")
        cv_file = st.file_uploader("CV (PDF, DOC, DOCX) *", type=["pdf", "doc", "docx"])
        lettre = st.file_uploader("Lettre de motivation (optionnel)", type=["pdf", "doc", "docx"])
        
        # Message complémentaire
        message = st.text_area("Message complémentaire (optionnel)", height=100)
        
        # Consentement RGPD
        rgpd = st.checkbox("J'accepte que mes données soient traitées dans le cadre de ma candidature *")
        
        # Bouton de soumission
        submitted = st.form_submit_button(label="Envoyer ma candidature")
        
        if submitted:
            # Validation
            errors = []
            
            # Vérification des champs obligatoires
            if not nom:
                errors.append("Le nom est obligatoire")
            if not prenom:
                errors.append("Le prénom est obligatoire")
            if not email:
                errors.append("L'email est obligatoire")
            elif not validate_email(email):
                errors.append("Le format de l'email est invalide")
            if not telephone:
                errors.append("Le numéro de téléphone est obligatoire")
            elif not validate_phone(telephone):
                errors.append("Le format du numéro de téléphone est invalide")
            if not competences_input:
                errors.append("Les compétences sont obligatoires")
            if not cv_file:
                errors.append("Le CV est obligatoire")
            if not rgpd:
                errors.append("Vous devez accepter le traitement de vos données")
            
            if errors:
                # Affichage des erreurs
                for error in errors:
                    st.error(error)
            else:
                try:
                    # Préparation des compétences
                    competences_list = [comp.strip() for comp in competences_input.split(",") if comp.strip()]
                    
                    # Préparation des données du candidat
                    candidate_info = {
                        "nom": nom,
                        "prenom": prenom,
                        "email": email,
                        "telephone": telephone,
                        "adresse": adresse,
                        "ville": ville,
                        "formation": formation,
                        "experience": experience,
                        "competences": competences_list,
                        "disponibilite": disponibilite.strftime("%Y-%m-%d"),
                        "pretentions": pretentions,
                        "mobilite": mobilite,
                        "teletravail": teletravail,
                        "message": message,
                        "uploadDate": datetime.now().strftime("%Y-%m-%d"),
                        "job_id": job.get("id", "")  # ID de la fiche de poste
                    }
                    
                    # Sauvegarde temporaire du fichier CV
                    with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(cv_file.name)[1]) as tmp:
                        tmp.write(cv_file.getvalue())
                        tmp_path = tmp.name
                    
                    try:
                        # Appel à l'API pour ajouter le CV
                        with st.spinner("Envoi de votre candidature en cours..."):
                            response = add_cv(tmp_path, candidate_info)
                        
                        if isinstance(response, dict) and "error" in response:
                            st.error(f"Erreur lors de l'envoi de la candidature: {response['error']}")
                        else:
                            st.success("✅ Votre candidature a été envoyée avec succès! Nous vous contacterons prochainement.")
                            
                            # Redirection vers la page de candidatures après quelques secondes
                            time.sleep(2)
                            set_page("candidate_applications")
                            st.rerun()
                    
                    finally:
                        # Nettoyage du fichier temporaire
                        if os.path.exists(tmp_path):
                            os.unlink(tmp_path)
                
                except Exception as e:
                    st.error(f"Une erreur s'est produite lors de l'envoi de votre candidature: {str(e)}")

if __name__ == "__main__":
    render_job_details()