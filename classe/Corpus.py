import datetime
import pickle
from typing import Dict
from classe.Document import Document
from classe.Author import Author
import re
import pandas as pd

class Corpus:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self, corpus: str):
        if hasattr(self, 'initialized') and self.initialized:
            self.initialized = True
            self.nom = corpus
            self.documents = {}
            self.authors = {}
            self.id_counter = 0

    def add_document(self, document: Document):
        """Ajoute un document au corpus et met à jour les informations de l'auteur."""
        self.id_counter += 1
        self.documents[self.id_counter] = document

        author_name = document.auteur
        if author_name not in self.authors:
            self.authors[author_name] = Author(author_name, 1, {})
        else:
            self.authors[author_name].nb_docs += 1
        
    def save(self, filename: str):
        """Sauvegarde le corpus dans un fichier pickle."""
        with open(f'./code/data/{filename}', 'wb') as f:
            pickle.dump(self, f)

    def load(self, filename: str):
        """Charge un corpus depuis un fichier pickle."""
        with open(f'./code/data/{filename}', 'rb') as f:
            loaded_corpus = pickle.load(f)
            self.nom = loaded_corpus.nom
            self.documents = loaded_corpus.documents
            self.authors = loaded_corpus.authors
            self.id_counter = loaded_corpus.id_counter 
    
    def __repr__(self):
        """Représentation textuelle du corpus."""
        return f"Le sujet '{self.nom}' chargé avec {len(self.documents)} documents et {len(self.authors)} auteurs."
    
    def __getattribute__(self, name: str):
        """Permet d'accéder aux attributs de l'instance."""
        return super().__getattribute__(name)
    
    def sort_title_and_date(self):
        """Trie les documents par titre et date de publication."""
        return dict(sorted(self.documents.items(), key=lambda item: (item[1].titre, item[1].date_publication)))
    
    def search(self, keyword: str):
        """Recherche un mot-clé dans les titres et résumés des documents du corpus."""
        pattern = re.compile(re.escape(keyword), re.IGNORECASE)
        return {doc_id: doc for doc_id, doc in self.documents.items() if pattern.search(doc.titre) or pattern.search(doc.texte)}

    def concorde(self, keyword: str, size: int = 30):
        """Génère des concordances pour un mot-clé donné dans les documents du corpus."""
        pattern = re.compile(re.escape(keyword), re.IGNORECASE)
        concordances = pd.DataFrame(columns=['Document ID', 'left', 'keyword' ,'right'])

        for doc_id, doc in self.documents.items():
            for match in pattern.finditer(doc.texte):
                # Extraction du texte autour du mot-clé
                start, end = match.span()
                left_context = doc.texte[max(0, start - size):start].strip()
                right_context = doc.texte[end:(end + size)].strip()
                
                # Ajout de la concordance au DataFrame
                concordances = pd.concat([concordances, pd.DataFrame({'Document ID': [doc_id], 'left': [left_context], 'keyword': [match.group()], 'right': [right_context]})], ignore_index=True)
        
        return concordances