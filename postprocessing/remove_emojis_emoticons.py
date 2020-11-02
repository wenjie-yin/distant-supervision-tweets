import sys
import json
import re
from pathlib import Path
sys.path.append(str(Path('~/Projects/distant-supervision-tweets/').expanduser()))
from utils.regexes import emoticon_regex, url_regex, username_regex

# lower case, replace any space with white space, remove non-ascii, emoticon, username, url

input_filename = sys.argv[1]
output_filename = '{}-cleaned.txt'.format(input_filename.split('/')[-1].split('.')[-2])

with open(input_filename, 'r') as fi, open(output_filename, 'wb') as fo:
    for line in fi:
        line = line.strip()
        tweet = json.loads(line)
        text = tweet['text']
        text = ' '.join(text.split())
        text = text.encode('ascii', 'ignore').decode()
        text = re.sub(emoticon_regex, '', text)
        text = re.sub(url_regex, '', text)
        text = re.sub(username_regex, '', text)
        text = text.lower()
        text = text.strip()
        to_write = (text + '\n').encode('utf8')
        fo.write(to_write)

print('finished writing to {}'.format(output_filename))

