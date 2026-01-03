class Author():
    """Classe représentant un auteur."""
    
    def __init__(self, name:str, nb_docs:int, production:dict):
        self.name = name 
        self.nb_docs = nb_docs
        self.production = production
    
    def __str__(self):
        return self.name