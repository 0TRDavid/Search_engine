import pickle
from classe.Document import Document
from classe.Author import Author
import re
import pandas as pd
from scipy.sparse import csr_matrix
import numpy as np

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
    
    def clean_texte(self):
        """Nettoie le texte de tous les documents du corpus en supprimant les caractères spéciaux et retour à la ligne."""
        for doc in self.documents.values():
            cleaned_text = re.sub(r'http\S+|www\.\S+', '', doc.texte) # Nettoie les urls
            cleaned_text = re.sub(r'\s+', ' ', cleaned_text)  # Remplace les espaces multiples par un seul espace
            cleaned_text = re.sub(r'[^a-zA-Z0-9\s]', '', cleaned_text).lower()
            cleaned_text = re.sub(r'\n+', ' ', cleaned_text).strip()
            doc.texte = cleaned_text
    
    def build_vocab_et_frequences(self):
        """
        Parcourt le corpus une seule fois et construit :
        - self._vocab : set de tous les mots
        - self._term_counts : dict avec nombre total d'occurrences
        - self._doc_counts : dict avec nombre de documents contenant le mot
        """
        self._vocab = set()
        self._term_counts = {}
        self._doc_counts = {}

        for doc in self.documents.values():
            words = re.findall(r'\b\w+\b', doc.texte.lower())
            self._vocab.update(words)
            seen_in_doc = set()
            for word in words:
                self._term_counts[word] = self._term_counts.get(word, 0) + 1
                if word not in seen_in_doc:
                    self._doc_counts[word] = self._doc_counts.get(word, 0) + 1
                    seen_in_doc.add(word)

    def get_vocabulaire(self):
        """Renvoie la liste triée du vocabulaire déjà construit."""
        return sorted(self._vocab)

    def frequences(self):
        """
        Renvoie un DataFrame avec :
        - id : identifiant unique du mot
        - mot : le mot du vocabulaire
        - term_frequency : nombre total d'occurrences dans le corpus
        - document_frequency : nombre de documents contenant le mot
        """
        vocab = list(self._vocab)
        freq_df = pd.DataFrame({
            'id': range(len(vocab)),  # identifiant unique
            'mot': vocab,
            'term_frequency': [self._term_counts[word] for word in vocab],
            'document_frequency': [self._doc_counts[word] for word in vocab]
        }).sort_values(by='term_frequency', ascending=False).reset_index(drop=True)

        return freq_df

    def build_tf_matrix_from_vocab(self):
        """
        Construit la matrice Documents x Termes (TF) en utilisant directement
        la liste de vocabulaire et les identifiants fournis par frequences().
        """
        # Récupérer le DataFrame des fréquences
        freq_df = self.frequences()

        # Créer un dictionnaire mot -> id
        vocab = {row['mot']: row['id'] for _, row in freq_df.iterrows()}
        n_docs = len(self.documents)
        n_terms = len(vocab)
        rows, cols, data = [], [], []

        # Parcourir les documents et compter les occurrences
        for doc_idx, doc in enumerate(self.documents.values()):
            words = re.findall(r'\b\w+\b', doc.texte.lower())
            doc_term_count = {}
            for word in words:
                if word in vocab:
                    term_id = vocab[word]
                    doc_term_count[term_id] = doc_term_count.get(term_id, 0) + 1
            for term_id, count in doc_term_count.items():
                rows.append(doc_idx)
                cols.append(term_id)
                data.append(count)

        # Construire la matrice sparse
        self.TF = csr_matrix((data, (rows, cols)), shape=(n_docs, n_terms), dtype=int)
        return self.TF
