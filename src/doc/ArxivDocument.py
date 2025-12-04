from src.doc.Document import Document
from datetime import datetime   

class ArxivDocument(Document):
    def __init__(self, titre:str, auteur:str, date_publication:datetime, contenu:str, url:str, co_auteur:list):
        super().__init__(titre, auteur, date_publication, url, contenu)
        self.co_auteur = co_auteur
        self.type = "arxiv"
    
    def __str__(self):
        return f"Objet ArxivDocument, hérité de Document : {self.titre} avec {self.co_auteur}"
    
    