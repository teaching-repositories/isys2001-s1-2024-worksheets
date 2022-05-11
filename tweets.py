# Imports
import snscrape.modules.twitter as sntwitter
import pandas as pd
import re


def clean(text):
  ''' Uses regular expresison to extract english letter and digits from the supplied text. '''
  regExp = "(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)"
  return ' '.join(re.sub(regExp, " ", text).split())


def tweets_to_csv(what, since='2022-01-01', until='2022-02-31', max_tweets = 500, csv_file='tweets.csv'):
  '''
  Performs a simple term based search of twitter tweets to
  save the date and message of the tweet.

  Parameters
  ----------
  what: str
    The search term
  since: str, YYYY-MM-DD, optional
    The date to start search from (default 2022-01-01)
  until: str, YYYY-MM-DD, optional
    The date to search to (default 2022-01-31)
  max_tweets: int, optional
    The maximum number of tweets to return (default 500)

  '''
  _get_tweets(what, since, until, max_tweets, csv_file)



def tweets_to_df(what, since='2022-01-01', until='2022-01-31', max_tweets = 500):
  '''
  Performs a simple term based search of twitter tweets to get
  the date and message of the tweet.

  Parameters
  ----------
  what: str
    The search term
  since: str, YYYY-MM-DD, optional
    The date to start search from (default 2022-01-01)
  until: str, YYYY-MM-DD, optional
    The date to search to (default 2022-01-31)
  max_tweets: int, optional
    The maximum number of tweets to return (default 500)

  Returns
  -------
  Pandas Dataframe of date and the tweet message.  The message has
  been *cleaned* to remove emojis and non english letters.

  '''
  return _get_tweets(what, since, until, max_tweets, csv_file=None)



def _get_tweets(what, since, until, max_tweets, csv_file=None):
  '''
  Internal function to performs a simple term based search of twitter tweets to get
  the date and message of the tweet.

  Parameters
  ----------
  what: str
    The search term
  since: str, YYYY-MM-DD
    The date to start search from
  until: str, YYYY-MM-DD, optional
    The date to search to
  max_tweets: int, optional
    The maximum number of tweets to return
  csv_file: str, optional
    Name of file to save data frame to

  Returns
  -------
  If no file name supplied then returns a Pandas Dataframe
  of date and the tweet message.  The message has
  been *cleaned* to remove emojis and non english letters.

  '''
  # Using TwitterSearchScraper to scrape data and append tweets to list
  query = sntwitter.TwitterSearchScraper(f'{what} since:{since} until:{until}').get_items()
  tweet_data = [next(query) for _ in range(max_tweets)]
  tweets = [[tweet.date, tweet.id, tweet.content] for tweet in tweet_data ]

  # Creating a dataframe from the tweets list above
  tweets_df = pd.DataFrame(tweets, columns=['Datetime', 'Tweet Id', 'Text'])

  # Clean the data
  tweets_df['Clean Text'] = tweets_df['Text'].apply(clean)
  tweets_df['Date'] = pd.to_datetime(tweets_df['Datetime']).dt.date

  if csv_file == None:
    return tweets_df[['Date','Clean Text']]
  else:
    return tweets_df[['Date','Clean Text']].to_csv(file_loc)
