from code_v2.scrapping_arxiv import scrapping_arxiv
from code_v2.scrapping_reddit import scrapping_reddit
from classe.Corpus import Corpus

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

    #save_corpus(sujet)
    load_corpus(sujet)
    
    