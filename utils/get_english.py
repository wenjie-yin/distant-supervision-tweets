import json
import sys

if len(sys.argv) < 2:
    sys.exit()

fname = sys.argv[1]
count = 0

with open(fname, 'r') as fall, open(fname.replace('.json', '-eng.json'), 'w') as feng:
    for line in fall:
        line = line.strip()
        try:
            tweet = json.loads(line)
            if 'text' in tweet and 'lang' in tweet and tweet['lang'] == 'en':
                feng.write(line + '\n')
            count += 1
            #if count >= 200:
                #break
        except:
            continue
        
	
