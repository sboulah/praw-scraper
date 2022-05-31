# Import Needed Libraries
from dhooks import Webhook, Embed
from configparser import ConfigParser
from collections import deque
import time
import threading
import praw
import os

# Config
config = ConfigParser()
config.read('config.ini')

# Reddit OAuth
reddit = praw.Reddit(client_id=config.get('REDDIT_AUTH', 'REDDIT_ID'),
                     client_secret=config.get('REDDIT_AUTH', 'REDDIT_SECRET'),
                     user_agent=config.get('REDDIT_AUTH', 'REDDIT_AGENT'))

# Matches
matches = ['gfycat', 'jpg', 'png']

# Webhook color and setup
embed = Embed(
    color=0x0000FF,
    timestamp='now'
    )

# Create Bot
def bot():
    submission_seen = deque(maxlen=11)
    while True:
        try:
            for submission in reddit.subreddit('pics').hot(limit=10):
                if submission.permalink not in submission_seen and any(x in submission.url for x in matches):
                    submission_seen.append(submission.permalink)
                    embed.set_author(name=str(submission.title), url='https://www.reddit.com' + str(submission.permalink))
                    embed.set_footer(text='/r/' + str(submission.subreddit) + ' • Made by Sami')
                    embed.set_image(str(submission.url))
                    Webhook(config.get('WEBHOOKS', 'DISCORD_WEBHOOK')).send(embed=embed)
                    time.sleep(1)
        except Exception as e: print(e)

# Start Bot
thread1 = threading.Thread(target=bot)
thread1.start()