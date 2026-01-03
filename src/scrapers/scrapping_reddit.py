import praw
from datetime import datetime
from src.doc.RedditDocument import RedditDocument

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

        doc = RedditDocument(titre, auteur, date_pub, texte, url, nb_comments)
        documents.append(doc)

    return documents