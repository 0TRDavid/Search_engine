import re
import numpy as np
import pandas as pd
from tqdm import tqdm

class SearchEngine:
    def __init__(self, corpus):
        self.corpus = corpus

    def vectorise_request(self, query: str):
        """
        Transforme une requête en un vecteur de poids TF-IDF.
        Le vecteur est basé sur le vocabulaire et les IDF du corpus.
        """
        # Nettoyage de la requête (similaire à clean_texte)
        query = query.lower()
        query = re.sub(r'[^\w\s]', ' ', query)
        query = re.sub(r'\s+', ' ', query).strip()
        
        mots_requete = query.split()
        vecteur_requete = np.zeros(len(self.corpus.vocab))
        
        # Calcul des Term Frequencies (TF) locaux pour la requête
        tf_local = {}
        for mot in tqdm(mots_requete, desc="Vectorisation de la requête"):
            if mot in self.corpus.vocab:
                mot_id = self.corpus.vocab[mot]['id']
                tf_local[mot_id] = tf_local.get(mot_id, 0) + 1
                
        # Application des poids TF-IDF
        # Pour chaque mot de la requête, on calcule le poids TF-IDF: TF * IDF
        for mot_id, tf in tqdm(tf_local.items(), desc="Calcul des poids TF-IDF pour la requête"):
            # Récupération de l'IDF (log(N / (df + 1)))
            N = len(self.corpus.documents)
            df = self.corpus.vocab[list(self.corpus.vocab.keys())[mot_id]]['doc_frequency']
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
        if self.corpus.mat_TF_IDF is None:
            self.corpus.mat_TFxIDF()

        vecteur_requete = self.vectorise_request(query)
        
        # Si le vecteur requête est nul, aucun mot n'est dans le vocabulaire
        if np.linalg.norm(vecteur_requete) == 0:
            print("Aucun mot de votre requête n'a été trouvé dans le vocabulaire du corpus.")
            return []

        # Calcul des similarités cosinus entre la requête et les documents
        correction = 1*10e-10  # Pour éviter la division par zéro
        produits_scalaires = self.corpus.mat_TF_IDF.dot(vecteur_requete) # Calculer le produit scalaire (numérateur de la similarité cosinus)
        norme_requete = np.linalg.norm(vecteur_requete) # Calculer la similarité cosinus (normalisation par les normes)
        normes_documents = np.sqrt(self.corpus.mat_TF_IDF.power(2).sum(axis=1).A1)
        similarites = produits_scalaires / (norme_requete * normes_documents + correction)

        # Trier les scores et afficher les meilleurs résultats
        doc_ids = list(self.corpus.documents.keys()) #Lier les ID aux documents
        results_df = pd.DataFrame({'doc_id': doc_ids, 'score_similarite': similarites}) # Tri par score décroissant
        results_df = results_df.sort_values(by='score_similarite', ascending=False) # Tri par score décroissant
        
        # Filtrer les scores supérieurs à 0
        results_df = results_df[results_df['score_similarite'] > 0]
                
        top_results = []
        for index, row in results_df.head(top_n).iterrows():
            doc_id = row['doc_id']
            score = float(row['score_similarite'])
            doc = self.corpus.documents[doc_id]
            top_results.append((doc.titre, doc.url ,f'{round(score*100)}%'))
            
        return top_results