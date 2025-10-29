import datetime

class Document:
    def __init__(self, titre: str, auteur: str, date_publication: datetime.datetime, url: str, texte: str):
        self.titre = titre
        self.auteur = auteur
        self.date_publication = date_publication
        self.url = url
        self.texte = texte
        self.type = None

    def __str__(self):
        return f"{self.titre}"
    
    def get_type(self):
        return self.type
