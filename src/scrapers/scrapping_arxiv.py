import ssl
import certifi
import urllib.request
import xmltodict
from datetime import datetime
from src.doc.ArxivDocument import ArxivDocument

def scrapping_arxiv(query: str):
    context = ssl.create_default_context(cafile=certifi.where())
    url = f'http://export.arxiv.org/api/query?search_query=all:{query}&start=0&max_results=1000'

    with urllib.request.urlopen(url, context=context) as response:
        data = response.read().decode("utf-8")

    parsed_data = xmltodict.parse(data)["feed"]["entry"]

    documents = []
    for article in parsed_data:
        titre = article.get("title", "").strip()
        texte = article.get("summary", "").strip()
        url_article = article.get("id", "")
        auteur_data = article.get("author")
        date_pub = article.get("published", "")

        # Récupérer seulement le premier auteur et les co-auteurs
        if isinstance(auteur_data, list):
            auteur = auteur_data[0].get("name", "") if "name" in auteur_data[0] else ""
            co_auteur = [a.get("name", "") for a in auteur_data[1:]] if len(auteur_data) > 1 else []
        else:
            auteur = auteur_data.get("name", "") if auteur_data else ""
        
        try:
            date_pub = datetime.fromisoformat(date_pub.replace("Z", "+00:00"))
        except Exception:
            date_pub = None

        # Création de l’objet Document
        documents.append(ArxivDocument(titre, auteur, date_pub, url_article, texte, co_auteur))

    return documents


if __name__ == "__main__":
    liste_docs = scrapping_arxiv()
    for d in liste_docs[:5]:
        print(d)
