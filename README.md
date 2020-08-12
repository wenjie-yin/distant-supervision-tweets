# methods.py
contains:
  - Criterion: a criterion to judge whether a single text sentence falls into any of the possible categories.
    - KeywordCriterion: a type of criterion that uses keywords. keywords can be defined using a dict.
  - DistantSupervisor: applies a Criterion to an input file and categorise all tweets in that file, creating a new file for each category. option to also include what evidence based on which it categorised each tweet.
# extract_tweets_by_keywords.py
example script for using a KeywordCriterion to categorise tweets into positive and negative based on emoticons and emojis.
# analyse_keywords.py
example script for counting how many times each keyword was used as evidence to categorise a tweet (if any) and the how many keywords were found in each categorised tweet.
