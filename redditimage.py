__author__ = 'Ion'
import praw as p
import random

def redditimage(choice):
    user_agent = ("IRC Image Fetcher Bot by /u/Embossing_Mat")
    r = p.Reddit(user_agent=user_agent)
    link = random.choice(list(r.get_subreddit(choice).get_hot(limit=10)))
    if link.over_18 == True:
        nsfw = True
    else:
        nsfw = False
    print(link)
    return link.url, nsfw


def randnsfw():
    user_agent = ("IRC Image Fetcher Bot by /u/Embossing_Mat")
    r = p.Reddit(user_agent=user_agent)
    subreddit = r.get_random_subreddit(nsfw=True)
    return subreddit._url