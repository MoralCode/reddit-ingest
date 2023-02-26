import argparse
import datetime
import json
import time
import requests
from os import getenv
from dotenv import load_dotenv
import praw
from sqlalchemy import text
from SQLiteConnection import engine
from wtfrit_storage_schema import CommentVibes, Vibes, Database
from praw.models import Submission

#set up the parser
parser = argparse.ArgumentParser()

parser.add_argument('--link')

#parse the arguments
args = parser.parse_args()

load_dotenv(dotenv_path='./key.env')

reddit = praw.Reddit(
    client_id = getenv("client_id"),
    client_secret = getenv("secret_key"),
    user_agent = "WTFRIT",
)

db = Database()
db.initialize()

def scrapeReddit():
    db.reset_values()          
    six_months_ago = int(time.time()) - (6 * 30 * 24 * 60 * 60)
    subreddit = reddit.subreddit('rit')
    for submission in subreddit.hot(params={'before': six_months_ago, 't': 'month'}):
        if submission.selftext != "" and submission.score >= 5:
            data = {'text': submission.selftext}
            sentiment = requests.post('http://127.0.0.1:4000/sentiment', json=data)
            sentiment_score = json.loads(sentiment.text)['sentiment']
            total_sentiment = sentiment_score
            if submission.score !=0:
                total_votes=int(submission.score/submission.upvote_ratio)
            else:
                total_votes=0
            post = Vibes(title = submission.title, contents=submission.selftext, upvotes=submission.score, total_votes=total_votes, sentiment=int(sentiment_score*100), source_url=submission.url, last_updated= datetime.datetime.fromtimestamp(int(submission.created_utc)))
            db.add(post)
            if submission.comments != []:
                #for each comment
                for post in submission.comments:
                    if post.body != "" or post.body != None:
                        comment_data = {'text': post.body}
                        comment_sentiment = requests.post('http://127.0.0.1:4000/sentiment', json=comment_data)
                        comment_sentiment_score = json.loads(comment_sentiment.text)['sentiment']
                        comment_post = CommentVibes(parent_id = submission.id, contents=post.body, sentiment=int(comment_sentiment_score*100))
                        db.add(comment_post)
                        total_sentiment = total_sentiment + comment_sentiment_score
                submission_sentiment = total_sentiment / (submission.num_comments + 1)
                submission.sentiment = submission_sentiment
            db.commit()



def scrapeTest():
    submission = Submission(reddit=reddit, url=args.link)
    data = {'text': submission.selftext}
    sentiment = requests.post('http://127.0.0.1:4000/sentiment', json=data)
    sentiment_score = json.loads(sentiment.text)['sentiment']
    post = Vibes(title = submission.title, contents=submission.selftext, upvotes=submission.score, total_votes=int(submission.score/submission.upvote_ratio), sentiment=int(sentiment_score*100), source_url= submission.url, last_updated= datetime.datetime.fromtimestamp(int(submission.created_utc)))
    db.add(post)
    db.commit()

if args.link is None:
    scrapeReddit()
else:
    scrapeTest()

