import praw
import pandas as pd

reddit = praw.Reddit(client_id='E3FjjdQyw-pTDH6NPz2_fQ', client_secret='_LB7q9pXdQt81h7MOkQRy73BjJEMDQ', user_agent='Brasier0')
posts = []
ml_subreddit = reddit.subreddit('MachineLearning')

for post in ml_subreddit.hot(limit=10):
    print(post)
    posts.append([post.title, post.score, post.id, post.subreddit, post.url, post.num_comments, post.selftext, post.created])
posts = pd.DataFrame(posts,columns=['title', 'score', 'id', 'subreddit', 'url', 'num_comments', 'body', 'created'])
print(posts)
