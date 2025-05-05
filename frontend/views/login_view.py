import streamlit as st
import re
from utils.api import register_user, login_user
from utils.styles import load_css
from utils.session_manager import set_page, initialize_session_state

def validate_email(email):
    """Valide le format de l'email"""
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return bool(re.match(pattern, email))

def validate_password(password):
    """Vérifie que le mot de passe a au moins 6 caractères"""
    return len(password) >= 6

def render_login_view():
    """Affiche la page de connexion/inscription"""
    initialize_session_state()
    load_css()

    st.image("static/images/hiro.png", width=150)
    
    st.markdown("""
    <div style="text-align: center; margin-bottom: 30px;">
        <h1 style="color: #00A8A8;">Plateforme de recrutement, performé avec Hiro</h1>
    </div>
    """, unsafe_allow_html=True)
    
    # Onglets pour choisir entre connexion et inscription
    tab1, tab2 = st.tabs(["Connexion", "Inscription"])
    
    # Onglet Connexion
    with tab1:
        with st.form("login_form"):
            st.subheader("Connexion")
            email = st.text_input("Email")
            password = st.text_input("Mot de passe", type="password")
            
            col1, col2 = st.columns(2)
            with col1:
                user_type = st.radio("Je suis un :", ["Candidat", "Recruteur"])
            
            submitted = st.form_submit_button("Se connecter")
            
            if submitted:
                if not email or not password:
                    st.error("Veuillez remplir tous les champs.")
                elif not validate_email(email):
                    st.error("Format d'email invalide.")
                else:
                    # Conversion du type d'utilisateur pour l'API
                    user_type_api = "candidate" if user_type == "Candidat" else "recruiter"
                    
                    # Appel à l'API de connexion
                    response = login_user(email, password)
                    
                    if isinstance(response, dict) and "error" in response:
                        st.error(f"Erreur de connexion : {response['error']}")
                    elif isinstance(response, dict) and "message" in response and response["message"] == "Connexion réussie":
                        # Stocker les informations utilisateur en session
                        st.session_state.user = response.get("user", {})
                        st.session_state.user_type = user_type_api
                        
                        # Rediriger vers la page appropriée
                        if user_type_api == "candidate":
                            set_page("candidate_home")
                        else:
                            set_page("recruiter_dashboard")
                        
                        st.success("Connexion réussie!")
                        st.rerun()
                    else:
                        st.error("Erreur lors de la connexion. Veuillez réessayer.")
    
    # Onglet Inscription
    with tab2:
        with st.form("register_form"):
            st.subheader("Inscription")
            
            col1, col2 = st.columns(2)
            with col1:
                prenom = st.text_input("Prénom")
                email = st.text_input("Email", key="reg_email")
            
            with col2:
                nom = st.text_input("Nom")
                password = st.text_input("Mot de passe", type="password", key="reg_password")
            
            col1, col2 = st.columns(2)
            with col1:
                user_type = st.radio("Je m'inscris en tant que :", ["Candidat", "Recruteur"], key="reg_type")
            
            submitted = st.form_submit_button("S'inscrire")
            
            if submitted:
                if not email or not password or not nom or not prenom:
                    st.error("Veuillez remplir tous les champs.")
                elif not validate_email(email):
                    st.error("Format d'email invalide.")
                elif not validate_password(password):
                    st.error("Le mot de passe doit contenir au moins 6 caractères.")
                else:
                    # Conversion du type d'utilisateur pour l'API
                    user_type_api = "candidate" if user_type == "Candidat" else "recruiter"
                    
                    # Appel à l'API d'inscription
                    response = register_user(email, password, nom, prenom)
                    
                    if isinstance(response, dict) and "error" in response:
                        st.error(f"Erreur d'inscription : {response['error']}")
                    elif isinstance(response, dict) and "message" in response and response["message"] == "Utilisateur créé":
                        st.success("Inscription réussie! Vous pouvez maintenant vous connecter.")
                    else:
                        st.error("Erreur lors de l'inscription. Veuillez réessayer.")
    
    # Pied de page
    st.markdown("""
    <div style="text-align: center; margin-top: 50px; color: #AAAAAA;">
        <p>© 2025 HiRo - Votre assistant RH intelligent</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    render_login_view()