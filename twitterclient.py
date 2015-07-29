import tweepy, time, sys
 


CONSUMER_KEY = 'vtJGsddeasdad8XxasdXoissdfaGbZGFwja'
CONSUMER_SECRET = 'spPs6oasdfMMLeZPsdfsdf1MsoCR4XLTGrSx3NPpzadfstnWaZqeo8OvnvYudzwA'
ACCESS_KEY = '33928246sdaf72-Y1IedCAsdfsdfs1KFIrEK3S1ZkyiuCSpcB2neTT3XepZUz'
ACCESS_SECRET = 'dg6zdfdsagG64TaTG86sCFQlYwCktitet6BZgfd7TQ0u7gg29xLjhv'
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)
 


api.update_with_media('face.png',status='Hello World')
