import sys
import json
import re
from pathlib import Path
sys.path.append(str(Path('~/Projects/distant-supervision-tweets/').expanduser()))
from utils.regexes import emoticon_regex, url_regex, username_regex, word_or_punct_regex

# lower case, replace any space with white space, remove non-ascii, emoticon, username, url

input_filename = sys.argv[1]
input_path = Path(input_filename)
parent = str(input_path.parent)
output_filename = '{}/{}-cleaned.txt'.format(parent, input_path.name.split('.')[-2])

with open(input_filename, 'r') as fi, open(output_filename, 'wb') as fo:
    for line in fi:
        try:
            line = line.strip()
            tweet = json.loads(line)
            text = tweet['text']
            if 'evidence' in tweet.keys():
                evidence_list = tweet['evidence']
                for evidence in evidence_list:
                    text = text.replace(evidence, '')
        except json.decoder.JSONDecodeError:
            text = line
        text = ' '.join(text.split())
        text = text.encode('ascii', 'ignore').decode()

        text = re.sub(emoticon_regex, '', text)
        text = re.sub(url_regex, '<url>', text)
        text = re.sub(username_regex, '<user>', text)

        # pad punctuations, then remove extra spaces
        text = re.sub(r'([#:\"\'.,!?()])', r' \1 ', text)
        text = re.sub('\s{2,}', ' ', text)

        text = text.lower()
        text = text.strip()

        if bool(re.search("[a-z]", text)):
            to_write = (text + '\n').encode('utf8')
            fo.write(to_write)

print('finished writing to {}'.format(output_filename))

