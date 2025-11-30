import praw
from datetime import datetime
from src.RedditDocument import RedditDocument

def scrapping_reddit(sujet: str):
    reddit = praw.Reddit(
        client_id='E3FjjdQyw-pTDH6NPz2_fQ',
        client_secret='_LB7q9pXdQt81h7MOkQRy73BjJEMDQ',
        user_agent='Brasier0'
    )

    documents = []
    ml_subreddit = reddit.subreddit(sujet)

    for post in ml_subreddit.hot(limit=100):
        titre = post.title
        auteur = str(post.author) if post.author else "inconnu"
        date_pub = datetime.fromtimestamp(post.created_utc)
        url = f"https://www.reddit.com{post.permalink}"
        texte = post.selftext.strip() if post.selftext else ""
        nb_comments = post.num_comments

        #doc = Document(titre, auteur, date_pub, url, texte)
        doc = RedditDocument(titre, auteur, date_pub, texte, url, nb_comments)
        documents.append(doc)

    return documents


if __name__ == "__main__":
    liste_docs = scrapping_reddit()
    for d in liste_docs[:5]:
        print(d)
