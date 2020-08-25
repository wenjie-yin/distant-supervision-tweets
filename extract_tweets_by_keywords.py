from utils.keywords import *
from methods import KeywordCriterion, DistantSupervisor
import argparse
import time


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('tweet_file', help='.json file containing each line a dict')
    parser.add_argument('--append_evidence', '-e', action='store_true', default=False,
                        help='append list of matched evidence for categorising')
    parser.add_argument('--print_progress', '-p', action='store_true', default=False,
                        help='print out progress')

    args = parser.parse_args()
    all_tweets_file = args.tweet_file
    append_evidence = args.append_evidence
    print_progress = args.print_progress

    keyword_criterion = KeywordCriterion(positive_negative, name="pos_neg_emo")
    supervisor = DistantSupervisor(all_tweets_file, keyword_criterion)

    started_time = time.time()
    supervisor.run(append_evidence=append_evidence, print_progress=print_progress)
    finished_time = time.time()
    print('finished. took {:.2f} seconds. '.format(finished_time - started_time))

