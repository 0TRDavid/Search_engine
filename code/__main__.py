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

    # Charger ou sauvegarder le corpus
    #save_corpus(sujet)
    load_corpus(sujet)

    print(sujet_corpus)
    
    # Liste de documents triés par titre et date
    sorted_docs = sujet_corpus.sort_title_and_date()
    #print(pd.DataFrame.from_dict({k: vars(v) for k, v in sorted_docs.items()}, orient='index'))
    
    # Exemple d'accès à un document et son type
    #print(sujet_corpus.documents[1].get_type())