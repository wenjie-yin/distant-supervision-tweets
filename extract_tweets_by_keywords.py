from utils.keywords import *
from methods import KeywordCriterion, DistantSupervisor
import argparse


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('tweet_file', help='.json file containing each line a dict')

    args = parser.parse_args()
    all_tweets_file = args.tweet_file

    keyword_criterion = KeywordCriterion(positive_negative, name="pos_neg_emo")
    supervisor = DistantSupervisor(all_tweets_file, keyword_criterion)

    supervisor.run()
