import json
import sys
import re

tokens = {'pos': [':)', ':-)', ': )', ':D', '=)'], 'neg': [':(', ':-(', ': (']}

if len(sys.argv) < 2:
    sys.exit()

fname = sys.argv[1]

alltweets = 0
postweets = 0
negtweets = 0
with open(fname, 'r') as fh, open(fname.replace('.json', '-pos.json'), 'w') as fwpos, open(fname.replace('.json', '-neg.json'), 'w') as fwneg:
    for line in fh:
        line = line.strip()
        try:
            tweet = json.loads(line)

            if 'text' in tweet and 'lang' in tweet and tweet['lang'] == 'en':
                alltweets += 1
                ispos = 0
                isneg = 0
                for keyword in tokens['pos']:
                    if keyword in tweet['text']:
                        ispos = 1
                for keyword in tokens['neg']:
                    if keyword in tweet['text']:
                        isneg = 1

                if ispos == 1 and isneg == 0:
                    postweets += 1
                    fwpos.write(line + '\n')

                if isneg == 1 and ispos == 0:
                    negtweets += 1
                    fwneg.write(line + '\n')

                print(fname + ' - all: ' + str(alltweets) + ' - pos: ' + str(postweets) + ' - neg: ' + str(negtweets), end='\r')
        except:
            continue

print(fname + ' - all: ' + str(alltweets) + ' - pos: ' + str(postweets) + ' - neg: ' + str(negtweets))
