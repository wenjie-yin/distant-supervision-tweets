import re
import json
from collections import defaultdict

class DistantSupervisor:
    def __init__(self, input_file, criterion):
        self.input_filename = input_file
        self.criterion = criterion
        # self.criteria = [criterion]
        self.criterion_type = self.criterion.name
        # self.criterion_types = [criterion.name for criterion in self.criteria]
        self.output_filenames = ['{}-{}-{}.json'.format(self.input_filename.split('.json')[0], self.criterion.name, category)
                                 for category in self.criterion.categories]
        self.output_fs = dict()
        self.counts = defaultdict(int)

    def run(self):
        self.open_output_files()

        with open(self.input_filename) as input_f:
            for line in input_f:
                line = line.strip()
                try:
                    tweet = json.loads(line)

                    if all(['text' in tweet, 'lang' in tweet, tweet['lang'] == 'en', 'retweeted_status' not in tweet]):

                        category, evidence = self.criterion.categorise(tweet['text'])

                        if category is not None:
                            tweet['evidence'] = evidence
                            self.output_fs[category].write(json.dumps(tweet) + '\n')
                            self.counts[category] += 1
                            self.counts['total'] += 1

                        print('{}-{}'.format(self.input_filename, self.criterion_type) +
                              ', '.join(['-{}: {}'.format(category, count) for category, count in self.counts.items()]),
                              end='\r')
                except:
                    continue

        print('{}-{}'.format(self.input_filename, self.criterion_type) +
              ', '.join(['-{}: {}'.format(category, count) for category, count in self.counts.items()]))

        self.close_output_files()

    def open_output_files(self):
        for filename, category in zip(self.output_filenames, self.criterion.categories):
            self.output_fs[category] = open(filename, 'w')

    def close_output_files(self):
        for output_f in self.output_fs.values():
            output_f.close()


class Criterion:
    def __init__(self):
        self.name = 'Dummy'
        self.categories = None
        self.num_of_categories = None

    def categorise(self, tweet, return_evidence=True):
        raise NotImplementedError


class KeywordCriterion(Criterion):
    def __init__(self, keywords, name='Keyword'):
        super().__init__()
        self.name = name
        self.keywords = keywords
        self.categories = list(self.keywords.keys())
        self.num_of_categories = len(self.categories)

    def categorise(self, tweet, return_evidence=True):
        tweet_category = None
        if return_evidence:
            evidence = list()
            for category in self.categories:
                for keyword in self.keywords[category]:
                    if keyword in tweet:
                        if tweet_category not in [None, category]:
                            return None, None
                        tweet_category = category
                        evidence.append(keyword)

            return tweet_category, evidence

        else:
            for category in self.categories:
                for keyword in self.keywords[category]:
                    if keyword in tweet:
                        if tweet_category is not None:
                            return None
                        tweet_category = category
                        break

            return tweet_category
