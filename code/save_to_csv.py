import pandas as pd
from scrapping_arxiv import scrapping_arxiv
from scrapping_reddit import scrapping_reddit

# Récupération des données
reddit, arxiv = scrapping_reddit(), scrapping_arxiv()

# Concaténation + colonne index + sauvegarde
docs = pd.concat([reddit, arxiv], ignore_index=True)
docs.insert(0, "index", range(1, len(docs) + 1))
docs.to_csv("./code/data/docs.csv",sep='\t', index=False, encoding="utf-8")


