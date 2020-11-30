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
        except json.decoder.JSONDecodeError:
            text = line
        text = ' '.join(text.split())
        text = text.encode('ascii', 'ignore').decode()

        # using placeholders first, so that there is no interaction with the next step
        text = re.sub(url_regex, 'aurlthatis', text)
        text = re.sub(username_regex, 'auserthatis', text)

        # this way potential emoticons can be separated from text before removing e.g. lol:(
        text = ' '.join(re.findall(word_or_punct_regex, text))
        text = re.sub(emoticon_regex, '', text)

        # pad punctuations, then remove extra spaces
        text = re.sub(r'([^\w\s])', r' \1 ', text)
        text = re.sub('\s{2,}', ' ', text)

        text = text.replace('aurlthatis', '<url>')
        text = text.replace('auserthatis', '<user>')

        text = text.lower()
        text = text.strip()

        if bool(re.search("[a-z]", text)):
            to_write = (text + '\n').encode('utf8')
            fo.write(to_write)

print('finished writing to {}'.format(output_filename))

