import datetime
import pickle
from typing import Dict
from classe.Document import Document
from classe.Author import Author


class Corpus:
    def __init__(self, corpus: str):
        self.nom = corpus
        self.documents = {}
        self.authors = {}
        self.id_counter = 0

    def add_document(self, document: Document):
        self.id_counter += 1
        self.documents[self.id_counter] = document

        author_name = document.auteur
        if author_name not in self.authors:
            self.authors[author_name] = Author(author_name, 1, {})
        else:
            self.authors[author_name].nb_docs += 1
        
    def save(self, filename: str):
        with open(f'./code/data/{filename}', 'wb') as f:
            pickle.dump(self, f)

    def load(self, filename: str):
        with open(f'./code/data/{filename}', 'rb') as f:
            loaded_corpus = pickle.load(f)
            self.nom = loaded_corpus.nom
            self.documents = loaded_corpus.documents
            self.authors = loaded_corpus.authors
            self.id_counter = loaded_corpus.id_counter 
    
    def __repr__(self):
        return f"Le sujet '{self.nom}' chargé avec {len(self.documents)} documents et {len(self.authors)} auteurs."
    
    def __getattribute__(self, name):
        return super().__getattribute__(name)
    
    def sort_title_and_date(self):
        return dict(sorted(self.documents.items(), key=lambda item: (item[1].titre, item[1].date_publication)))

