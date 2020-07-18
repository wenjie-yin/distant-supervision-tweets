import json

tokens = {'pos': [':)', ':-)', ': )', ':D', '=)'], 'neg': [':(', ':-(', ': (']}

poscount = 0
negcount = 0
with open('all/all-pos.json', 'r') as fh:
    for line in fh:
        poscount += 1
        line = line.strip()
        tweet = json.loads(line)
        tweetid = tweet['id_str']
        tweettext = tweet['text']
        timestamp = tweet['created_at']
        category = 'positive'

        cleantext = tweettext.replace('\n', ' ').replace('\t', ' ')
        for token in tokens['pos']:
            cleantext = cleantext.replace(token, ' ')

        newjson = tweet
        newjson['label'] = 'positive'
        newjson['cleantext'] = cleantext

        fileid = tweetid[:-16].zfill(3)
        with open('sentiment-txt/sentiment-' + fileid + '.txt', 'a') as fw:
            fw.write(tweetid + '\t' + timestamp + '\t' + category + '\t' + cleantext + '\n')
        with open('sentiment-json/sentiment-' + fileid + '.json', 'a') as fw:
            fw.write(json.dumps(newjson) + '\n')

        print('Positive: ' + str(poscount), end='\r')
    print('Positive: ' + str(poscount))

with open('all/all-neg.json', 'r') as fh:
    for line in fh:
        negcount += 1
        line = line.strip()
        tweet = json.loads(line)
        tweetid = tweet['id_str']
        tweettext = tweet['text']
        timestamp = tweet['created_at']
        category = 'negative'

        cleantext = tweettext.replace('\n', ' ').replace('\t', ' ')
        for token in tokens['neg']:
            cleantext = cleantext.replace(token, ' ')

        newjson = tweet
        newjson['label'] = 'negative'
        newjson['cleantext'] = cleantext

        fileid = tweetid[:-16].zfill(3)
        with open('sentiment-txt/sentiment-' + fileid + '.txt', 'a') as fw:
            fw.write(tweetid + '\t' + timestamp + '\t' + category + '\t' + cleantext + '\n')
        with open('sentiment-json/sentiment-' + fileid + '.json', 'a') as fw:
            fw.write(json.dumps(newjson) + '\n')

        print('Negative: ' + str(negcount), end='\r')
    print('Negative: ' + str(negcount))
