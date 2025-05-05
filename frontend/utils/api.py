import urllib3
from utils.api_client import ApiClient

# Désactiver les avertissements de certificat non vérifié pour le développement
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Wrapper d'API exposant les fonctionnalités de l'API client
# Cela permet d'avoir un point d'accès unique et facilement modifiable

def register_user(email, password, nom="", prenom=""):
    """Enregistre un nouvel utilisateur."""
    return ApiClient.register_user(email, password, nom, prenom)

def login_user(email, password):
    """Authentifie un utilisateur."""
    return ApiClient.login_user(email, password)

def generate_fiche_api(titre, secteur, contrat, niveau, competences):
    """Génère une fiche de poste via l'API."""
    job_data = {
        "titre": titre,
        "secteur": secteur,
        "contrat": contrat,
        "niveau": niveau,
        "competences": competences
    }
    return ApiClient.generate_job_posting(job_data)

def get_job_postings():
    """Récupère toutes les fiches de poste."""
    return ApiClient.get_job_postings()

def get_job_posting(job_id):
    """Récupère une fiche de poste spécifique."""
    return ApiClient.get_job_posting(job_id)

def add_cv(cv_path, candidate_info):
    """Ajoute un CV pour un candidat."""
    return ApiClient.add_cv(cv_path, candidate_info)

def match_candidates(job_id):
    """Trouve les meilleurs candidats pour une fiche de poste."""
    return ApiClient.match_candidates(job_id)

def get_candidates():
    """Récupère tous les candidats."""
    return ApiClient.get_candidates()

def get_candidate(candidate_id):
    """Récupère un candidat spécifique."""
    return ApiClient.get_candidate(candidate_id)

def analyze_cv(cv_path, fiche_id=None):
    """Analyse un CV, optionnellement par rapport à une fiche de poste."""
    return ApiClient.analyze_cv(cv_path, fiche_id)

def get_candidate_applications(candidate_email):
    """Récupère les candidatures d'un candidat."""
    return ApiClient.get_candidate_applications(candidate_email)

def update_application_status(application_id, new_status):
    """Met à jour le statut d'une candidature."""
    return ApiClient.update_application_status(application_id, new_status)