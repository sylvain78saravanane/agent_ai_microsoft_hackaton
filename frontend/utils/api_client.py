import requests
import urllib3
import os
import tempfile

# Désactiver les avertissements de certificat non vérifié pour le développement
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# URL de l'API
API_URL = "https://127.0.0.1:8443"

class ApiClient:
    """Client API pour communiquer avec le backend."""
    
    @staticmethod
    def register_user(email, password, nom="", prenom=""):
        """Enregistre un nouvel utilisateur."""
        url = f"{API_URL}/register"
        payload = {
            "userEmail": email,
            "password": password,
            "nom": nom,
            "prenom": prenom
        }
        
        try:
            response = requests.post(url, json=payload, verify=False)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": str(e)}

    @staticmethod
    def login_user(email, password):
        """Authentifie un utilisateur."""
        url = f"{API_URL}/login"
        payload = {
            "userEmail": email,
            "password": password
        }
        
        try:
            response = requests.post(url, json=payload, verify=False)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": str(e)}

    @staticmethod
    def generate_job_posting(job_data):
        """Génère une fiche de poste."""
        url = f"{API_URL}/generate_fiche"
        
        payload = {
            "titre": job_data.get("titre", ""),
            "secteur": job_data.get("secteur", ""),
            "contrat": job_data.get("contrat", ""),
            "niveau": job_data.get("niveau", ""),
            "competences": job_data.get("competences", "")
        }
        
        try:
            response = requests.post(url, json=payload, verify=False, timeout=100)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": str(e)}

    @staticmethod
    def get_job_postings():
        """Récupère toutes les fiches de poste."""
        url = f"{API_URL}/list_job_descriptions"
        
        try:
            response = requests.get(url, verify=False)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": str(e)}

    @staticmethod
    def get_job_posting(job_id):
        """Récupère une fiche de poste spécifique."""
        # Cette méthode nécessiterait un endpoint spécifique sur le backend
        # Pour l'instant, on récupère toutes les fiches et on filtre
        try:
            all_jobs = ApiClient.get_job_postings()
            if isinstance(all_jobs, dict) and "error" in all_jobs:
                return all_jobs
            
            for job in all_jobs:
                if job.get("id") == job_id or job.get("ficheId") == job_id:
                    return job
            
            return {"error": "Fiche de poste non trouvée"}
        except Exception as e:
            return {"error": str(e)}

    @staticmethod
    def add_cv(cv_path, candidate_info):
        """Ajoute un CV pour un candidat."""
        url = f"{API_URL}/add_cv"
        
        try:
            # Préparer les fichiers et les données
            files = {'cv_file': open(cv_path, 'rb')}
            
            # Convertir les compétences en liste si c'est une chaîne
            if isinstance(candidate_info.get("competences"), str):
                candidate_info["competences"] = [comp.strip() for comp in candidate_info["competences"].split(",")]
            
            # Appel API
            response = requests.post(url, files=files, data=candidate_info, verify=False)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": str(e)}
        finally:
            # S'assurer que le fichier est fermé
            if 'files' in locals() and 'cv_file' in files:
                files['cv_file'].close()

    @staticmethod
    def match_candidates(job_id):
        """Trouve les meilleurs candidats pour une fiche de poste."""
        url = f"{API_URL}/match_candidates/{job_id}"
        
        try:
            response = requests.get(url, verify=False)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": str(e)}

    @staticmethod
    def get_candidates():
        """Récupère tous les candidats."""
        # Cette méthode nécessiterait un endpoint spécifique sur le backend
        # Pour l'instant, c'est une méthode placeholder
        return {"error": "Endpoint non implémenté"}


    @staticmethod
    def analyze_cv(cv_path, fiche_id=None):
        """Analyse un CV, optionnellement par rapport à une fiche de poste."""
        # Cette méthode nécessiterait un endpoint spécifique sur le backend
        # Pour l'instant, c'est une méthode placeholder
        return {"error": "Endpoint non implémenté"}

    @staticmethod
    def get_candidate_applications(candidate_email):
        """Récupère les candidatures d'un candidat."""
        # Cette méthode nécessiterait un endpoint spécifique sur le backend
        # Pour l'instant, c'est une méthode placeholder
        return {"error": "Endpoint non implémenté"}

    @staticmethod
    def update_application_status(application_id, new_status):
        """Met à jour le statut d'une candidature."""
        # Cette méthode nécessiterait un endpoint spécifique sur le backend
        # Pour l'instant, c'est une méthode placeholder
        return {"error": "Endpoint non implémenté"}