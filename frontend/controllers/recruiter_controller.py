import streamlit as st
from utils.api import generate_fiche_api, get_job_postings, match_candidates, add_cv
import os
import tempfile
from datetime import datetime

class RecruiterController:
    """Contrôleur pour gérer les fonctionnalités du portail recruteur."""
    
    @staticmethod
    def generate_job_posting(job_data):
        """Génère une nouvelle fiche de poste."""
        # Vérification des données
        if not job_data.get("titre") or not job_data.get("secteur") or not job_data.get("contrat") or not job_data.get("niveau") or not job_data.get("competences"):
            return False, "Tous les champs sont obligatoires.", None
        
        try:
            # Appel à l'API
            response = generate_fiche_api(
                titre=job_data.get("titre"),
                secteur=job_data.get("secteur"),
                contrat=job_data.get("contrat"),
                niveau=job_data.get("niveau"),
                competences=job_data.get("competences")
            )
            
            if isinstance(response, dict) and "error" in response:
                return False, response["error"], None
            
            # Créer un objet JobPosting à partir de la réponse
            if isinstance(response, dict):
                job = {
                    "id": response.get("id", ""),
                    "titre": job_data.get("titre"),
                    "secteur": job_data.get("secteur"),
                    "contrat": job_data.get("contrat"),
                    "niveau": job_data.get("niveau"),
                    "competences": job_data.get("competences"),
                    "fichierPDF": response.get("fichierPDF", ""),
                    "content": response.get("fiche", ""),
                }
                return True, "Fiche de poste générée avec succès.", job
            else:
                return False, "Format de réponse inattendu de l'API.", None
                
        except Exception as e:
            return False, f"Erreur lors de la génération: {str(e)}", None
    
    @staticmethod
    def get_all_job_postings():
        """Récupère toutes les fiches de poste."""
        try:
            # Appel à l'API
            response = get_job_postings()
            
            if isinstance(response, dict) and "error" in response:
                return False, response["error"], []
            
            # Convertir les réponses en objets JobPosting
            job_postings = []
            if isinstance(response, list):
                for job_data in response:
                    # Vérifier si les données minimales sont présentes
                    if job_data.get("id") and job_data.get("titre"):
                        job = {
                            "id": job_data.get("id"),
                            "titre": job_data.get("titre"),
                            "secteur": job_data.get("secteur", "Non spécifié"),
                            "contrat": job_data.get("contrat", "Non spécifié"),
                            "niveau": job_data.get("niveau", "Non spécifié"),
                            "competences": job_data.get("competences", []),
                            "fichierPDF": job_data.get("fichierPDF", None),
                            "content": job_data.get("content", ""),
                        }
                        job_postings.append(job)
            
            return True, f"{len(job_postings)} fiches de poste trouvées.", job_postings
            
        except Exception as e:
            return False, f"Erreur lors de la récupération des fiches: {str(e)}", []
    
    @staticmethod
    def delete_job_posting(job_id):
        """Supprime une fiche de poste."""
        # Cette fonctionnalité nécessiterait un endpoint API
        # Pour l'instant, c'est une méthode placeholder
        return False, "Fonctionnalité non implémentée.", None
    
    @staticmethod
    def match_candidates_for_job(job_id):
        """Trouve les meilleurs candidats pour une fiche de poste."""
        try:
            # Appel à l'API
            response = match_candidates(job_id)
            
            if isinstance(response, dict) and "error" in response:
                return False, response["error"], []
            
            # Récupérer la liste des candidats correspondants
            matching_candidates = []
            if isinstance(response, list):
                for candidate_data in response:
                    candidate = {
                        "id": candidate_data.get("id", ""),
                        "nom": candidate_data.get("nom", ""),
                        "prenom": candidate_data.get("prenom", ""),
                        "email": candidate_data.get("email", ""),
                        "competences": candidate_data.get("competences", []),
                        "match_score": candidate_data.get("match_score", 0),
                        "competences_communes": candidate_data.get("competences_communes", [])
                    }
                    matching_candidates.append(candidate)
            
            return True, f"{len(matching_candidates)} candidat(s) correspondant(s) trouvé(s).", matching_candidates
            
        except Exception as e:
            return False, f"Erreur lors de la recherche de candidats: {str(e)}", []
    
    @staticmethod
    def analyze_cv(cv_file, job_id=None):
        """Analyse un CV, optionnellement par rapport à une fiche de poste."""
        # Sauvegarder temporairement le fichier CV
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(cv_file.name)[1]) as tmp:
            tmp.write(cv_file.getvalue())
            tmp_path = tmp.name
        
        try:
            # Préparation des données minimales pour l'API
            # En situation réelle, cela serait remplacé par un appel à une API d'analyse
            candidate_info = {
                "nom": "Analyse",
                "prenom": "Temporaire",
                "email": f"analyse_{datetime.now().strftime('%Y%m%d%H%M%S')}@temp.com",
                "competences": []
            }
            
            # Appel à l'API pour ajouter le CV (à remplacer par une API d'analyse)
            response = add_cv(tmp_path, candidate_info)
            
            if isinstance(response, dict) and "error" in response:
                return False, response["error"], None
            
            # Simuler une analyse de CV (à remplacer par une vraie analyse)
            analysis = {
                "score": 85,  # Score fictif
                "competences_detectees": ["Python", "JavaScript", "React", "Node.js", "SQL"],
                "points_forts": "Expérience en développement web, connaissances des frameworks modernes",
                "points_amelioration": "Expérience en gestion de projet limitée",
                "recommandation": "Profil intéressant pour des postes de développeur"
            }
            
            return True, "Analyse du CV effectuée avec succès.", analysis
            
        except Exception as e:
            return False, f"Erreur lors de l'analyse du CV: {str(e)}", None
        finally:
            # Nettoyer le fichier temporaire
            if os.path.exists(tmp_path):
                os.unlink(tmp_path)
    
    @staticmethod
    def update_candidate_status(application_id, new_status):
        """Met à jour le statut d'une candidature."""
        # Cette fonctionnalité nécessiterait un endpoint API
        # Pour l'instant, c'est une méthode placeholder
        return False, "Fonctionnalité non implémentée.", None
    
    @staticmethod
    def get_recruiter_statistics():
        """Récupère les statistiques pour le tableau de bord recruteur."""
        # En situation réelle, ces données proviendraient d'une API
        stats = {
            "postes_ouverts": 12,
            "candidatures_recues": 87,
            "entretiens_planifies": 9,
            "taux_conversion": 15.3,  # Pourcentage
            "temps_moyen_recrutement": 28  # Jours
        }
        
        return True, "Statistiques récupérées avec succès.", stats