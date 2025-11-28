from code.scrapping_arxiv import scrapping_arxiv
from code.scrapping_reddit import scrapping_reddit
from classe.Corpus import Corpus
import pandas as pd

def save_corpus(sujet):
    a, b = scrapping_reddit(sujet), scrapping_arxiv(sujet)
    liste = a + b

    for doc in liste:
        sujet_corpus.add_document(doc)

    sujet_corpus.save(f"{sujet}_corpus.pkl")

def load_corpus(sujet):
    sujet_corpus.load(f"{sujet}_corpus.pkl")

if __name__=="__main__":
    sujet = "MachineLearning"
    sujet_corpus = Corpus(sujet)
    
    # Vérification du singleton
    #sujet_2 = Corpus(sujet)
    #print(sujet_corpus is sujet_2)  

    # Charger ou sauvegarder le corpus
    #save_corpus(sujet)
    load_corpus(sujet)

    # Liste de documents triés par titre et date
    # sorted_docs = sujet_corpus.sort_title_and_date()
    #print(pd.DataFrame.from_dict({k: vars(v) for k, v in sorted_docs.items()}, orient='index'))
    
    # Exemple d'accès à un document et son type
    #print(sujet_corpus.documents[1].get_type())

    # Exemple de recherche dans le corpus
    """ results = sujet_corpus.search("learning")
    print(f"Documents trouvés pour le mot-clé 'learning': {len(results)}")
    for doc_id, doc in results.items():
        print(f"ID: {doc_id}, Titre: {doc.titre}")"""

    # Exemple de génération de concordances
    """concordances_df = sujet_corpus.concorde("learning", size=30)
    print(concordances_df)  """

    # Exemple de représentation textuelle du corpus
    sujet_corpus.clean_texte()
    sujet_corpus.construire_vocab()

    """print(sujet_corpus.vocab)
    print(len(sujet_corpus.vocab))"""

    sujet_corpus.mat_TF()
    sujet_corpus.calculer_stats_vocabulaire()
    #print(sujet_corpus.vocab)

    sujet_corpus.mat_TFxIDF()
    #print(sujet_corpus.mat_TFxIDF())
    

    