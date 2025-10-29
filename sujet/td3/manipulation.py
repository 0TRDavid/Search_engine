import pandas as pd

df = pd.read_csv(r'./code/data/docs.csv', sep="\t")
df["summary"] = df["summary"].astype(str)

print(f'taille du document {len(df)}')

df["nb_mots"] = df["summary"].apply(lambda x: len(x.split()))
df["nb_phrases"] = df["summary"].apply(lambda x: len([s for s in x.split('.') if s.strip() != ""]))
df = df[df["summary"].str.len() >= 20].reset_index(drop=True)
corpus = " ".join(df["summary"].tolist())

print(df.head())