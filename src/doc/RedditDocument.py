from src.doc.Document import Document
from datetime import datetime

class RedditDocument(Document):
    """Classe représentant un document Reddit, hérité de Document."""

    def __init__(self, titre:str, auteur:str, date_publication:datetime, contenu:str, url:str, nb_comments:int):
        super().__init__(titre, auteur, date_publication, url, contenu)
        self.nb_comments = nb_comments
        self.type = "reddit"
    
    def __str__(self):
        return f"Objet RedditDocument, hérité de Document : {self.titre} avec {self.nb_comments} commentaires"
        