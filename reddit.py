# Import the libraries that we need
from dhooks import Webhook, Embed
from configparser import ConfigParser
from collections import deque
import time
import threading
import praw
import os

config = ConfigParser()
config.read('config.ini')

# Reddit OAuth and API setup
reddit = praw.Reddit(client_id=config.get('REDDIT_AUTH', 'REDDIT_id'),
                     client_secret=config.get('REDDIT_AUTH', 'REDDIT_SECRET'),
                     user_agent=config.get('REDDIT_AUTH', 'REDDIT_AGENT'))

# Matches
matches = ['gfycat', 'jpg', 'png']

# Webhook color and setup
embed = Embed(
    color=0x0000FF,
    timestamp='now'
    )

def Loop():
    submission_seen = deque(maxlen=11)
    while True:
        try:
            for submission in reddit.subreddit('pics').hot(limit=10):
                if submission.permalink not in submission_seen and any(x in submission.url for x in matches):
                    submission_seen.append(submission.permalink)
                    embed.set_author(name=str(submission.title), url='https://www.reddit.com' + str(submission.permalink))
                    embed.set_footer(text='/r/' + str(submission.subreddit) + ' • Made by Sami, v5.0')
                    embed.set_image(str(submission.url))
                    Webhook(config.get('WEBHOOKS', 'discord_webhook')).send(embed=embed)
                    time.sleep(1)
        except Exception as e: print(e)

thread1 = threading.Thread(target=Loop)
thread1.start()