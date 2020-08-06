import json
import sys

if len(sys.argv) < 2:
    sys.exit()

fname = sys.argv[1]

with open(fname, 'r') as fall, open(fname.replace('.json', '-eng.json'), 'w') as feng:
    for line in fh:
        line = line.strip()
        try:
            tweet = json.loads(line)
            if 'text' in tweet and 'lang' in tweet and tweet['lang'] == 'en':
                feng.write(line + '\n')
        except:
            continue

