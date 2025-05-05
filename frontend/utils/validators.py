import re
from datetime import datetime

def validate_email(email):
    """Valide le format d'un email."""
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return bool(re.match(pattern, email))

def validate_password(password):
    """Valide la complexité d'un mot de passe."""
    # Au moins 6 caractères
    if len(password) < 6:
        return False
    return True

def validate_phone(phone):
    """Valide le format d'un numéro de téléphone.
    
    Accepte les formats:
    - 0612345678
    - 06 12 34 56 78
    - +33612345678
    - +33 6 12 34 56 78
    """
    # Supprimer les espaces, tirets et points
    clean_phone = re.sub(r'[\s.-]', '', phone)
    
    # Format français sans indicatif international
    if re.match(r'^0[1-9]\d{8}$', clean_phone):
        return True
    
    # Format international (France)
    if re.match(r'^\+33[1-9]\d{8}$', clean_phone):
        return True
    
    # Format international (général)
    if re.match(r'^\+\d{10,15}$', clean_phone):
        return True
    
    return False

def validate_not_empty(text):
    """Vérifie qu'un champ n'est pas vide."""
    return bool(text and text.strip())

def validate_job_form(job_data):
    """Valide les données d'une fiche de poste."""
    required_fields = ['titre', 'secteur', 'contrat', 'niveau', 'competences']
    
    for field in required_fields:
        if not validate_not_empty(job_data.get(field, '')):
            return False, f"Le champ '{field}' est obligatoire."
    
    return True, ""

def validate_candidate_form(candidate_data, cv_file=None):
    """Valide les données d'un candidat."""
    required_fields = ['nom', 'prenom', 'email', 'competences']
    
    for field in required_fields:
        if not validate_not_empty(candidate_data.get(field, '')):
            return False, f"Le champ '{field}' est obligatoire."
    
    if not validate_email(candidate_data.get('email', '')):
        return False, "Format d'email invalide."
    
    if 'telephone' in candidate_data and candidate_data['telephone'] and not validate_phone(candidate_data['telephone']):
        return False, "Format de numéro de téléphone invalide."
    
    if cv_file is not None and cv_file.name == '':
        return False, "Veuillez télécharger votre CV."
    
    return True, ""

def format_date(date_obj=None, format_str="%d/%m/%Y"):
    """Formate une date selon le format spécifié."""
    if date_obj is None:
        date_obj = datetime.now()
    
    if isinstance(date_obj, str):
        try:
            date_obj = datetime.strptime(date_obj, "%Y-%m-%d")
        except ValueError:
            try:
                date_obj = datetime.strptime(date_obj, "%d/%m/%Y")
            except ValueError:
                return date_obj  # Retourne la chaîne originale si le format n'est pas reconnu
    
    return date_obj.strftime(format_str)

def extract_competences_from_description(description):
    """Extrait les compétences potentielles à partir d'une description de poste.
    
    Cette fonction utilise des règles simples pour identifier les compétences
    dans une description textuelle. En production, cette fonction devrait être
    remplacée par une approche basée sur l'IA ou des modèles NLP.
    """
    # Liste de compétences techniques courantes à rechercher
    common_skills = [
        "Python", "Java", "JavaScript", "C#", "C++", "React", "Angular", "Vue.js",
        "Node.js", "PHP", "Ruby", "Swift", "Kotlin", "SQL", "NoSQL", "MongoDB",
        "MySQL", "PostgreSQL", "Oracle", "Django", "Flask", "Spring", "ASP.NET",
        "Docker", "Kubernetes", "AWS", "Azure", "GCP", "HTML", "CSS", "Git",
        "DevOps", "CI/CD", "Agile", "Scrum", "Machine Learning", "Data Science",
        "Deep Learning", "TensorFlow", "PyTorch", "NLP", "Computer Vision",
        "Big Data", "Hadoop", "Spark", "Tableau", "Power BI", "Excel",
        "Word", "PowerPoint", "Linux", "Windows", "macOS", "Android", "iOS",
        "REST API", "GraphQL", "Microservices", "Testing", "QA", "UX/UI",
        "Adobe Photoshop", "Adobe Illustrator", "Figma", "Sketch"
    ]
    
    # Extraire les compétences mentionnées dans la description
    found_skills = []
    description_lower = description.lower()
    
    for skill in common_skills:
        if skill.lower() in description_lower:
            found_skills.append(skill)
    
    # Rechercher les compétences avec le format "compétence en X"
    skill_patterns = [
        r'compétences? en ([A-Za-z0-9\+\#\s]+)',
        r'maîtrise (?:de|du|de la) ([A-Za-z0-9\+\#\s]+)',
        r'connaissances? (?:de|en|du|de la) ([A-Za-z0-9\+\#\s]+)'
    ]
    
    for pattern in skill_patterns:
        matches = re.finditer(pattern, description_lower)
        for match in matches:
            skill = match.group(1).strip().capitalize()
            if len(skill) > 2 and skill not in [s.lower() for s in found_skills]:
                found_skills.append(skill)
    
    return found_skills

def calculate_matching_score(job_competences, candidate_competences):
    """Calcule un score de correspondance entre les compétences requises pour un poste et celles d'un candidat.
    
    Args:
        job_competences (list): Liste des compétences requises pour le poste
        candidate_competences (list): Liste des compétences du candidat
        
    Returns:
        tuple: (score en pourcentage, liste des compétences communes)
    """
    # Normaliser les listes de compétences (minuscules pour la comparaison)
    if isinstance(job_competences, str):
        job_competences = [comp.strip() for comp in job_competences.split(",")]
    
    if isinstance(candidate_competences, str):
        candidate_competences = [comp.strip() for comp in candidate_competences.split(",")]
    
    job_comp_normalized = [comp.lower() for comp in job_competences if comp.strip()]
    candidate_comp_normalized = [comp.lower() for comp in candidate_competences if comp.strip()]
    
    # Calcul des compétences communes et du score
    common_skills = []
    for job_skill in job_comp_normalized:
        for candidate_skill in candidate_comp_normalized:
            # Correspondance exacte
            if job_skill == candidate_skill:
                if job_skill not in [s.lower() for s in common_skills]:
                    common_skills.append(job_skill)
                break
            
            # Correspondance partielle (une compétence contient l'autre)
            elif job_skill in candidate_skill or candidate_skill in job_skill:
                match_score = min(len(job_skill), len(candidate_skill)) / max(len(job_skill), len(candidate_skill))
                # Si au moins 70% de correspondance partielle
                if match_score >= 0.7 and job_skill not in [s.lower() for s in common_skills]:
                    common_skills.append(job_skill)
                    break
    
    # Calcul du score final
    if not job_comp_normalized:
        return 0, []
    
    score = (len(common_skills) / len(job_comp_normalized)) * 100
    
    # Inclure les versions originales des compétences communes (pour l'affichage)
    original_common_skills = []
    for common in common_skills:
        for orig in job_competences:
            if orig.lower() == common:
                original_common_skills.append(orig)
                break
    
    return round(score, 1), original_common_skills

def format_matching_score(score):
    """Formate un score de matching pour l'affichage.
    
    Args:
        score (float ou int): Score de matching en pourcentage
        
    Returns:
        tuple: (score formaté, classe CSS, message descriptif)
    """
    score_num = float(score) if isinstance(score, (int, float, str)) else 0
    
    # Formatage du score
    score_str = f"{score_num:.1f}%" if isinstance(score_num, float) else f"{score_num}%"
    
    # Classe CSS selon le score
    if score_num >= 80:
        css_class = "score-excellent"
        message = "Excellent match"
    elif score_num >= 70:
        css_class = "score-bon"
        message = "Bon match"
    elif score_num >= 50:
        css_class = "score-moyen"
        message = "Match acceptable"
    else:
        css_class = "score-faible"
        message = "Match faible"
    
    return score_str, css_class, message