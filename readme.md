# Moteur de Recherche (Reddit & Arxiv)

Ce projet consiste à développer un moteur de recherche d'information sans utiliser de bibliothèques comme scikit-learn ou NLTK. Il collecte des données textuelles depuis Reddit et Arxiv pour construire un corpus et permettre des recherches basées sur la similarité textuelle (TF-IDF).

## Objectifs
- **Acquisition** : Extraire des documents via les APIs de Reddit (librairie `praw`) et Arxiv (`urllib` et `xmltodict`).
- **Stockage** : Organiser les données en classes et sauvegarder le corpus au format Pickle pour éviter les appels API répétitifs.
- **Analyse** : Nettoyer le texte, construire un vocabulaire et générer une matrice TF-IDF.
- **Moteur de recherche** : Implémenter une recherche par similarité cosinus entre une requête et les documents.

## Pré-requis
- Python 3.12
- Les dépendances listées dans `requirements.txt` 

## Installation et Lancement

1. **Créer l'environnement virtuel et installer les dépendances** :
```bash
python -m venv env

# Windows
env\Scripts\activate

# Linux/Mac
source env/bin/activate

pip install -r requirements.txt
```

2. **Configuration** :
Le script `main.py` est configuré par défaut pour le sujet "NoSQL". Vous pouvez modifier cette variable dans le bloc `if __name__ == "__main__":`.

3. **Exécuter le programme** :
```bash
python main.py
```

4. **Utiliser l'interface graphique**: via interface.ipynb -> Partie 3 : Petite interface


## Structure du Projet

* `data/` : Dossier contenant les corpus sauvegardés (fichiers `.pkl`) + discours_US.csv pour le td8
* `src/scrapers/` : Scripts de récupération des données (Reddit & Arxiv).
* `src/doc/` : Définition des classes de documents
* `src/Corpus.py` : Gestion centralisée de la collection
* `src/SearchEngine.py` : Logique du moteur de recherche