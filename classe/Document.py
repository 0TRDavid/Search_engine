
class Document():
    def __init__(self, titre, auteur, date_publication, url, texte):
        self.titre = titre
        self.auteur = auteur
        self.date_publication = date_publication
        self.url = url 
        self.texte = texte

    def __str__(self):
        return print(Document)
    