import ssl
import certifi
import urllib.request
import xmltodict
import pandas as pd

def scrapping_arxiv():
    context = ssl.create_default_context(cafile=certifi.where())
    query = "MachineLearning"
    url = f'http://export.arxiv.org/api/query?search_query=all:{query}&start=0&max_results=1000'

    with urllib.request.urlopen(url, context=context) as response:
        data = response.read().decode("utf-8")

    parsed_data = xmltodict.parse(data)["feed"]["entry"]

    # Construction une liste de dictionnaires
    docs = []
    for article in parsed_data:
        docs.append({                
            "summary": article.get("summary", ""),     
            "source": "arxiv"                        
        })

    # Conversion en DataFrame
    df = pd.DataFrame(docs)
    return df

if __name__ == "__main__":
    df_articles = scrapping_arxiv()
    print(df_articles.head())
