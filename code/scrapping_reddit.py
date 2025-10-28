import praw
import pandas as pd

def scrapping_reddit():
    reddit = praw.Reddit(client_id='E3FjjdQyw-pTDH6NPz2_fQ', client_secret='_LB7q9pXdQt81h7MOkQRy73BjJEMDQ', user_agent='Brasier0')
    posts = []
    ml_subreddit = reddit.subreddit('MachineLearning')

    for post in ml_subreddit.hot(limit=100):
        posts.append([post.selftext, "reddit"])
    
    posts = pd.DataFrame(posts,columns=['summary', 'source'])
    return posts

if __name__=="__main__": 
    print(scrapping_reddit())