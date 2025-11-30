from src.Document import Document
from src.Author import Author
import re
import pickle
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
        if not hasattr(self, 'initialized'):
            self.initialized = True
            self.nom = corpus
            self.documents = {}
            self.authors = {}
            self.id_counter = 0
            # ajout de nouveaux attributs
            self.vocab = None
            self.mat_TF = None
            self.mat_TF_IDF = None
            self.cleaned = True

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
        with open(f'./data/{filename}', 'wb') as f:
            pickle.dump(self, f)

    def load(self, filename: str):
        """Charge un corpus depuis un fichier pickle."""
        with open(f'./data/{filename}', 'rb') as f:
            loaded_corpus = pickle.load(f)
            self.nom = loaded_corpus.nom
            self.documents = loaded_corpus.documents
            self.authors = loaded_corpus.authors
            self.id_counter = loaded_corpus.id_counter 
    
    def __repr__(self):
        """Représentation textuelle du corpus."""
        return f"Le sujet '{self.nom}' chargé avec {len(self.documents)} documents et {len(self.authors)} auteurs."
        
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
        """Nettoie le texte : minuscules, suppression ponctuation/URL, gestion accents."""
        for doc in self.documents.values():
            texte = doc.texte.lower() # Mise en minuscule
            texte = re.sub(r'http\S+|www\.\S+', '', texte) # Supprime les URLs
            texte = re.sub(r'[^\w\s]', ' ', texte) # Remplace ponctuation par espace
            texte = re.sub(r'\s+', ' ', texte).strip() # Remplace multiples espaces par un seul
            doc.texte = texte
            self.cleaned = True

    def construire_vocab(self):
        """
        Construire le dictionnaire vocabulaire (vocab).
        Les clefs sont les mots, la valeur est un dico avec l'id unique.
        """
        # Nettoyage des textes
        if not hasattr(self, 'cleaned') or not self.cleaned:
            self.clean_texte()

        # Récupération de tous les mots uniques
        mots_uniques = set()
        for doc in self.documents.values():
            mots_uniques.update(doc.texte.split())
        mots_tries = sorted(list(mots_uniques))

        # Création du dictionnaire vocab
        self.vocab = {}
        for idx, mot in enumerate(mots_tries):
            self.vocab[mot] = {
                'id': idx,            
                'total_occurrence': 0,   
                'doc_frequency': 0       
            }

    def create_mat_TF(self):
        """
        Construire la matrice Documents x Mots (TF).
        """
        # Construction de la liste vocabulaire
        self.construire_vocab()

        n_docs, n_mots = len(self.documents), len(self.vocab)
        rows, cols, data = [], [], []

        for doc_idx, doc in enumerate(self.documents.values()):
            mots_list = doc.texte.split()          
            compte_local = {}

            for mot in mots_list:
                if mot in self.vocab:
                    mot_id = self.vocab[mot]['id']
                    # On utilise collections.Counter ou un dictionnaire pour compter facilement:
                    compte_local[mot_id] = compte_local.get(mot_id, 0) + 1
            
            # Remplissage des listes pour la matrice sparse
            for mot_id, count in compte_local.items():
                rows.append(doc_idx)
                cols.append(mot_id)
                data.append(count)

        # Création de la matrice (sparse matrix)
        self.mat_TF = csr_matrix((data, (rows, cols)), shape=(n_docs, n_mots), dtype=int)
        
        return self.mat_TF 

    def calculer_stats_vocabulaire(self):
        """
        À partir de la matrice mat_TF, calculer les stats globales 
        et mettre à jour le dictionnaire vocab.
        """
        if self.mat_TF is None:
             self.create_mat_TF()

        total_occurrences = self.mat_TF.sum(axis=0).A1 
        doc_frequencies = self.mat_TF.getnnz(axis=0)

        for mot, infos in self.vocab.items():
            #print(infos['id'])
            mot_id = infos['id']
            infos['total_occurrence'] = int(total_occurrences[mot_id])
            infos['doc_frequency'] = int(doc_frequencies[mot_id])

    def mat_TFxIDF(self):
        """
        Calcule et retourne la matrice TF-IDF à partir de la matrice TF.
        """
        if self.mat_TF is None:
             self.create_mat_TF()

        N, n_mots = len(self.documents), len(self.vocab)
        df_vector = np.zeros(n_mots) #Récupération des fréquences documentaires (DF) pour tous les mots
        for mot, infos in self.vocab.items():
            df_vector[infos['id']] = infos['doc_frequency']

        idf_vector = np.log(N / (df_vector + 1)) #Calcul du vecteur IDF pour tous les mots
        self.mat_TF_IDF = self.mat_TF.multiply(idf_vector) #Calcul de la matrice TF-IDF
        return self.mat_TF_IDF
    
    def vectoriser_requete(self, query: str):
        """
        Transforme une requête en un vecteur de poids TF-IDF.
        Le vecteur est basé sur le vocabulaire et les IDF du corpus.
        """
        # Nettoyage de la requête (similaire à clean_texte)
        query = query.lower()
        query = re.sub(r'[^\w\s]', ' ', query)
        query = re.sub(r'\s+', ' ', query).strip()
        
        mots_requete = query.split()
        vecteur_requete = np.zeros(len(self.vocab))
        
        # Calcul des Term Frequencies (TF) locaux pour la requête
        tf_local = {}
        for mot in mots_requete:
            if mot in self.vocab:
                mot_id = self.vocab[mot]['id']
                tf_local[mot_id] = tf_local.get(mot_id, 0) + 1
                
        # Application des poids TF-IDF
        # Pour chaque mot de la requête, on calcule le poids TF-IDF: TF * IDF
        for mot_id, tf in tf_local.items():
            # Récupération de l'IDF (log(N / (df + 1)))
            N = len(self.documents)
            df = self.vocab[list(self.vocab.keys())[mot_id]]['doc_frequency']
            idf = np.log(N / (df + 1))
            
            # Poids TF-IDF dans le vecteur requête
            vecteur_requete[mot_id] = tf * idf
            
        return vecteur_requete 
    
    def search_engine(self, query: str, top_n: int = 10):
        """
        Recherche des documents similaires à la requête de l'utilisateur.

        Args:
            query (str): La requête de recherche.
            top_n (int): Le nombre maximum de meilleurs résultats à retourner.
        """
        # Construction de la matrice TFxIDF
        if self.mat_TF_IDF is None:
            self.mat_TFxIDF()

        vecteur_requete = self.vectoriser_requete(query)
        
        # Si le vecteur requête est nul, aucun mot n'est dans le vocabulaire
        if np.linalg.norm(vecteur_requete) == 0:
            print("Aucun mot de votre requête n'a été trouvé dans le vocabulaire du corpus.")
            return []

        produits_scalaires = self.mat_TF_IDF.dot(vecteur_requete) # Calculer le produit scalaire (numérateur de la similarité cosinus)
        doc_ids = list(self.documents.keys()) #Lier les ID aux documents
        norme_requete = np.linalg.norm(vecteur_requete) # Calculer la similarité cosinus (normalisation par les normes)
        normes_documents = np.sqrt(self.mat_TF_IDF.power(2).sum(axis=1).A1) # Norme des vecteurs
        similarites = produits_scalaires / (norme_requete * normes_documents)
        similarites = np.nan_to_num(similarites) 

        # Trier les scores et afficher les meilleurs résultats
        results_df = pd.DataFrame({'doc_id': doc_ids, 'score_similarite': similarites}) # Tri par score décroissant
        results_df = results_df.sort_values(by='score_similarite', ascending=False) # Tri par score décroissant
        
        # Filtrer les scores supérieurs à 0
        results_df = results_df[results_df['score_similarite'] > 0]
        
        print(f"\n Résultats de la recherche pour : '{query}'")
        
        top_results = []
        for index, row in results_df.head(top_n).iterrows():
            doc_id = row['doc_id']
            score = row['score_similarite']
            doc = self.documents[doc_id]
            
            print(f"ID: {doc_id} | Score: {score:.4f} | Titre: {doc.titre}")
            top_results.append((doc_id, score, doc))
            
        return top_results