import argparse
import datetime
import requests
from os import getenv
from dotenv import load_dotenv
import praw
from SQLiteConnection import engine
from Tables import Vibes
from praw.models import Submission
from sqlalchemy.orm import sessionmaker

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

DBSession = sessionmaker(bind=engine)
session = DBSession()

if args.link is None:
    for submission in reddit.subreddit("rit").hot(limit=50):
        if submission.selftext != "":
            post = Vibes(title = submission.title, contents=submission.selftext, upvotes=submission.score, source_url=submission.url, last_updated= datetime.datetime.fromtimestamp(int(submission.created_utc)))
            session.add(post)
else:
    submission = Submission(reddit=reddit, url=args.link)
    post = Vibes(title = submission.title, contents=submission.selftext, upvotes=submission.score, source_url= submission.url, last_updated= datetime.datetime.fromtimestamp(int(submission.created_utc)))
    session.add(post)
session.commit()
