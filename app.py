import tweepy
import time
import config


auth = tweepy.OAuthHandler(config.consumer_key, config.consumer_secret)
auth.set_access_token(config.access_token, config.access_token_secret)

api = tweepy.API(auth, timeout=10)

public_tweets = api.home_timeline()


def limit_handler(Cursor):
    try:
        while True:
            yield Cursor.next()
    except StopIteration:
        pass
    except tweepy.RateLimitError:
        time.sleep(1000)


# Genrous Bot that follow back
def follow_back(name):
    # name = 'Richard Chakborty'
    for follower in limit_handler(tweepy.Cursor(api.followers).items()):
        if follower.name == name:
            follower.follow()
            break
    return 'done'


# Generous bot that likes a post
def liker(search_str, no_of_tweets):
    # search_str = 'Adversarial'
    # no_of_tweets = 25
    for tweet in limit_handler(tweepy.Cursor(api.search, search_str).items(no_of_tweets)):
        try:
            tweet.favorite()
            print('I Liked that tweet')
        except tweepy.TweepError as err:
            print(err.reason)
        except StopIteration:
            break
    return 'done'
