import tweepy, time, sys
 


CONSUMER_KEY = 'Z2YVOgSjXD6huf5lj1v1LMVyB'
CONSUMER_SECRET = 'ejkMRX1mR578EGxHuYAjoMDy6S5ko07L1ODv23F2xTW9Grx7Nl'
ACCESS_KEY = '3392824672-Y1IedCA1KFIrEK3S1ZkyiuCSpcB2neTT3XepZUz'
ACCESS_SECRET = 'dg6zgG64TaTG86CFQlYwCktitet6BZ7TQ0u7gg29xLjhv'
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)
 


api.update_status(status='Hello World')
