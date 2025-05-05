import os
import base64
from azure.cosmos import CosmosClient, exceptions
from azure.cosmos.partition_key import PartitionKey
from dotenv import load_dotenv
from backend.extract_cv import extract_cv_text
import uuid
import io
import reportlab.lib.pagesizes as pagesizes
import io
import reportlab.lib.pagesizes as pagesizes
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph
from markdown2 import markdown
import hashlib


load_dotenv()

def hash_password(password):
    return hashlib.sha256(password.encode('utf-8')).hexdigest()

class CosmosDBManager:
    def __init__(self):
        # Load environment variables from .env file
        self.endpoint = os.environ["AZURE_COSMOS_ENDPOINT"]
        self.key = os.environ["AZURE_COSMOS_KEY"]
        self.database_name = "HiRoDatabase"
        self.cv_container="Cvs"
        self.fiche_container="FichesDePostes"
        self.user_container="User"

        # Initialize Cosmos client
        self.client = CosmosClient(self.endpoint, credential=self.key)

        # Create or get the database (cv)

        try:
            self.database = self.client.create_database_if_not_exists(id=self.database_name)
        except exceptions.CosmosResourceExistsError:
            self.database = self.client.get_database_client(self.database_name)
            print(f"Database {self.database_name} existe déjà.")
        except exceptions.CosmosHttpResponseError as e:
            print(f"Erreur lors de la création de la base de données : {e}")
            raise

        # Create or get container for cv
        try:
            self.cv_container = self.database.create_container_if_not_exists(
                id=self.cv_container,
                partition_key=PartitionKey(path="/candidatId"),
                indexing_policy={
                    "includedPaths": [
                        {"path": "/*"},
                    ],
                },
            )
        except exceptions.CosmosResourceExistsError:
            self.cv_container = self.database.get_container_client(self.cv_container)
            print(f"Container {self.cv_container} existe déjà.")

        except exceptions.CosmosResourceNotFoundError:
            print(f="Container {self.cv_container} existe déjà.")
            raise

        except exceptions.CosmosHttpResponseError as e:
            print(f"Erreur lors de la création du conteneur cv : {e}")
            raise

  

        # Create or get the container for job postings (fiche)
        try :
            self.fiche_container = self.database.create_container_if_not_exists(
                id=self.fiche_container,
                partition_key=PartitionKey(path="/ficheId"),
                indexing_policy={
                    "includedPaths": [
                        {"path": "/*"},
                    ],
                },
            )
        except exceptions.CosmosResourceExistsError:
            self.fiche_container = self.database.get_container_client(self.fiche_container)
            print(f"Container {self.fiche_container} existe déjà.")
        except exceptions.CosmosResourceNotFoundError:
            print(f"Container {self.fiche_container} n'existe pas.")
        except exceptions.CosmosHttpResponseError as e:
            print(f"Erreur lors de la création du conteneur fiche de poste : {e}")
            raise

        '''
        -- create or get container for user

        '''
        try :
            container_id =  self.user_container
            self.user_container = self.database.create_container_if_not_exists(
                id = container_id,
                partition_key=PartitionKey(path="/userEmail"),
                indexing_policy={
                    "includedPaths": [
                        {"path": "/*"},
                    ],
                },
            )

        except exceptions.CosmosResourceExistsError:
            self.user_container = self.database.get_container_client(self.user_container)
            print(f"Container{self.user_container} n'existe pas")
        except exceptions.CosmosResourceNotFoundError:
            print(f"Container {self.user_container} n'existe pas.")
        except exceptions.CosmosHttpResponseError as e:
            print(f"Erreur lors de la création du conteneur fiche de poste : {e}")
            raise

    def add_user(self, user_info):

        try :
            hashed_password = hash_password(user_info["password"])

            document = {
                "id":user_info["userEmail"],
                "userEmail":user_info["userEmail"],
                "nom":user_info["nom"],
                "prenom":user_info["prenom"],
                "password":hashed_password
            }

            self.user_container.upsert_item(document)
            print("Utilisateur ajouté avec succès.")
            return user_info["userEmail"]

        except exceptions.CosmosHttpResponseError as e:
            print(f"Erreur lors de l'ajout de l'utilisateur : {e}")
            raise



    def get_user(self, user_info):
        try:
            userEmail = user_info["userEmail"]
            entered_password = user_info["password"]
            hashed_entered_password = hash_password(entered_password)
    
            # Query user by ID (partition key)
            query = f"SELECT * FROM c WHERE c.userEmail = '{userEmail}'"
            items = list(self.user_container.query_items(
                query=query,
                enable_cross_partition_query=True
            ))
    
            if not items:
                print("Utilisateur non trouvé.")
                return None
    
            user_doc = items[0]
    
            if user_doc["password"] == hashed_entered_password:
                print("Authentification réussie.")
                return user_doc
            else:
                print("Mot de passe incorrect.")
                return None
    
        except exceptions.CosmosHttpResponseError as e:
            print(f"Erreur lors de la récupération de l'utilisateur : {e}")
            raise
        

    def add_cv(self, cv_path, candidat_info):
           
           cv_text = extract_cv_text(cv_path)
               

           with open(cv_path, 'rb') as f:
               pdf_base64 = base64.b64encode(f.read()).decode('utf-8')
               

           source = candidat_info.get("source", "Unknown")

           id = str(uuid.uuid4())  # Generate a unique ID for the CV

           document = {
               "id": f"cv_{id}",
               "candidatId": candidat_info["email"],
               "nom": candidat_info["nom"],
               "prenom": candidat_info["prenom"],
               "email": candidat_info["email"],
               "competences": candidat_info["competences"],
               "fichierPDF": pdf_base64,
               "content": cv_text,
               "metadata": {
                   "source": source,
                   "upload_date": candidat_info.get("uploadDate")
               }
           }
        

           try :
               response = self.cv_container.upsert_item(body=document)
               return response["id"]  # Return the ID of the inserted item
           except exceptions.CosmosHttpResponseError as e:
               print(f"Erreur lors de l'ajout du CV : {e}")
               raise
           except exceptions.CosmosResourceExistsError as e:
               print(f"Erreur : le document existe déjà : {e}")
               raise
           

    @staticmethod
    def clean_duplicate_lines(text):
     seen = set()
     cleaned_lines = []
     for line in text.split('\n'):
         if line not in seen:
             cleaned_lines.append(line)
             seen.add(line)
     return "\n".join(cleaned_lines)
    
def generate_pdf_from_text(self, text):
    """Génère un PDF à partir du texte de la fiche de poste avec un formatage amélioré"""
    clean_text = self.clean_duplicate_lines(text)
    buffer = io.BytesIO()
    
    # Configurer le document PDF avec marges adaptées
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        leftMargin=40,
        rightMargin=40,
        topMargin=30,
        bottomMargin=30
    )
    
    # Styles pour le PDF
    styles = getSampleStyleSheet()
    
    # Style pour le titre principal
    title_style = ParagraphStyle(
        name='TitleStyle',
        parent=styles['Heading1'],
        fontSize=18,
        fontName="Helvetica-Bold",
        textColor=colors.HexColor("#006666"),
        alignment=1,  # Centré
        spaceAfter=15,
        spaceBefore=10,
        leading=22
    )
    
    # Style pour les sous-titres (sections)
    section_style = ParagraphStyle(
        name='SectionStyle',
        parent=styles['Heading2'],
        fontSize=14,
        fontName="Helvetica-Bold",
        textColor=colors.HexColor("#00A8A8"),
        spaceBefore=15,
        spaceAfter=8,
        leading=16
    )
    
    # Style pour le texte normal
    body_style = ParagraphStyle(
        name='BodyStyle',
        parent=styles['Normal'],
        fontSize=11,
        fontName="Helvetica",
        leading=14,
        spaceBefore=2,
        spaceAfter=8
    )
    
    # Style pour les listes
    list_style = ParagraphStyle(
        name='ListStyle',
        parent=styles['Normal'],
        fontSize=11,
        fontName="Helvetica",
        leftIndent=20,
        leading=14,
        spaceBefore=2,
        spaceAfter=2
    )
    
    # Style pour le pied de page
    footer_style = ParagraphStyle(
        name='FooterStyle',
        parent=styles['Normal'],
        fontSize=9,
        fontName="Helvetica-Oblique",
        textColor=colors.HexColor("#666666"),
        alignment=1,  # Centré
        spaceBefore=10
    )
    
    # Analyser le texte et construire les paragraphes
    elements = []
    
    # Ajouter un logo ou en-tête
    # elements.append(Image("path/to/logo.png", width=100, height=30))
    # elements.append(Spacer(1, 10))
    
    # Traiter chaque ligne du texte
    lines = clean_text.split('\n')
    in_list = False
    list_items = []
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        # Titre principal (première ligne contenant le titre du poste)
        if "FICHE DE POSTE" in line:
            elements.append(Paragraph(line, title_style))
            elements.append(Spacer(1, 10))
            continue
            
        # Sous-titres des sections (commencent par un numéro)
        if re.match(r"^[0-9]+\.\s", line) or line.startswith("##"):
            # Si on était dans une liste, on l'ajoute avant de passer à la section
            if in_list and list_items:
                for item in list_items:
                    elements.append(Paragraph(f"• {item}", list_style))
                list_items = []
                in_list = False
                elements.append(Spacer(1, 5))
                
            # Enlever les ## pour les titres en markdown
            if line.startswith("##"):
                line = line.replace("##", "").strip()
                
            elements.append(Paragraph(line, section_style))
            continue
            
        # Éléments de liste (commencent par un tiret ou une puce)
        if line.startswith("-") or line.startswith("•"):
            in_list = True
            # Enlever le marqueur de liste et les espaces
            line = line[1:].strip() if line.startswith("-") else line[1:].strip()
            list_items.append(line)
            continue
            
        # Texte normal
        # Si on était dans une liste, on l'ajoute avant de passer au texte normal
        if in_list and list_items:
            for item in list_items:
                elements.append(Paragraph(f"• {item}", list_style))
            list_items = []
            in_list = False
            elements.append(Spacer(1, 5))
            
        # Mise en valeur des mots clés
        if "**" in line:
            # Convertir ** en balises de gras pour ReportLab
            line = line.replace("**", "<b>", 1)
            line = line.replace("**", "</b>", 1)
            
        elements.append(Paragraph(line, body_style))
    
    # Ajouter un pied de page
    elements.append(Spacer(1, 20))
    elements.append(Paragraph("© HiRo Site - Confidentiel - Ne pas diffuser", footer_style))
    
    # Construire le document
    doc.build(elements)
    buffer.seek(0)
    
    # Convertir en Base64 pour le stockage
    pdf_base64 = base64.b64encode(buffer.read()).decode('utf-8')
    return pdf_base64

 ##    def generate_pdf_from_text(self, text):
## 
 ##        clean_text = self.clean_duplicate_lines(text)
 ##        buffer = io.BytesIO()
 ##        doc = SimpleDocTemplate(buffer, pagesize=pagesizes.A4)
 ##        elements = []
 ##        
 ##        style = getSampleStyleSheet()
 ##        
 ##        title_style = ParagraphStyle(
 ##         name='TitleStyle',
 ##         fontSize=18,
 ##         spaceAfter=12,
 ##         textColor=colors.HexColor("#2E86C1"),
 ##         alignment=1,
 ##         fontName="Helvetica-Bold"
 ##   )
 ##        body_style = ParagraphStyle(
 ##        name='BodyStyle',
 ##        fontSize=12, 
 ##        leading=14,
 ##        fontName="Helvetica",
 ##        textColor=colors.black,
 ##        spaceAfter=12,
 ## 
 ##   )
 ##        html_paragraph = markdown(text)
 ##        elements.append(Paragraph(html_paragraph, body_style))
 ##        
 ##        for para in clean_text.split("\n"):
 ##            para = para.strip()
 ##        if para:
 ##            elements.append(Paragraph(para, body_style))
 ##            doc.build(elements)
 ##            buffer.seek(0)
 ##            pdf_base64 = base64.b64encode(buffer.read()).decode('utf-8')
 ##        return pdf_base64


        
    def add_job_description(self, job_info, job_description):

        job_id = str(uuid.uuid4())  # Generate a unique ID for the job description"

        if not isinstance(job_description, str):
            raise ValueError("Le texte de la fiche de poste doit être une chaîne de caractères.")
        


        pdf_base64 = self.generate_pdf_from_text(job_description)

        document = {
            "id": f"fiche_de_poste_{job_info['titre']}_+{job_id}",
            "ficheId": job_id,
            "fichierPDF": pdf_base64,
            "titre": job_info["titre"],
            "secteur": job_info["secteur"],
            "contrat": job_info["contrat"],
            "niveau": job_info["niveau"],
            "competences": job_info["competences"],
            "content": job_description,
            "source": job_info["metadata"]["source"],
        }

        response = self.fiche_container.upsert_item(body=document)
        return response["id"]  # Return the ID of the inserted item
     
    def get_cv(self, email):
        """Recupere un CV par email du candidat"""
        query = f"SELECT * FROM c WHERE c.email = '{email}'"
        items = list(self.cv_container.query_items(
            query=query,
            enable_cross_partition_query=True
        ))
        return items[0] if items else None
        
        
    def get_job_description(self, keyword):
        """Recupere une fiche de poste par mot clé"""
        
        query = "SELECT * FROM c WHERE CONTAINS(c.id, 'keyword')"
        query = query.replace("keyword", keyword) 
        items = list(self.fiche_container.query_items(
            query=query,
            enable_cross_partition_query=True
        ))
        return items[0] if items else None
        
    def list_job_descriptions(self):
        """Recupere toutes les fiches de poste"""
        query = "SELECT * FROM c"
        items = list(self.fiche_container.query_items(
            query=query,
            enable_cross_partition_query=True
        ))
        return items
        
    def list_cvs(self):
        query = "SELECT * FROM c "
        items = list(self.cv_container.query_items(
            query=query,
            enable_cross_partition_query=True
        ))
        return items

    def search_cv_by_competence(self, competence):
        """Rechercher des CVs par compétence"""
        query = f"SELECT * FROM c WHERE ARRAY_CONTAINS(c.competences, '{competence}')"
        items = list(self.cv_container.query_items(
            query=query,
            enable_cross_partition_query=True
        ))
        return items

    def search_cv_by_vector(self,embedding, top_k=5):
        """Rechercher des CVs par vecteur d'embedding"""
        query={
            "vector": embedding,
            "topK": top_k,
            "fields": ["id", "candidatId", "nom", "prenom", "email", "competences"],
        }

        results = self.cv_container.query_items(
            query="SELECT * FROM c VECTOR_SEARCH c.embedding ANN SEARCH @vector TOP_K @topK WITH EMBEDDING",  
            parameters=[
                {"name": "@vector", "value": query["vector"]},
                {"name": "@topK", "value": query["topK"]}
            ],
            enable_cross_partition_query=True
        )
        return list(results)
    
if __name__ == "__main__":
    # Exemple d'utilisation de CosmosDBManager
    db_manager = CosmosDBManager()

    # Ajouter un CV (exemple)
    candidat_info = {
        "nom": "Potier",
        "prenom": "Benjamin",
        "email": "potier.benjamin@yoyo.com",
        "competences": ["Python", "Django"],
        "source": "LinkedIn",
        "uploadDate": "2025-04-24"
    }
    cv_path = "./data/cv/Chloé_Bernard_CV.pdf" 
    db_manager.add_cv(cv_path, candidat_info)

    # Lister les CVs
    cvs = db_manager.list_cvs()
    print("Liste des CVs :", cvs)
           








