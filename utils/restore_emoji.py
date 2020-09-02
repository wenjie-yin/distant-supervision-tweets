import json


class EmojiRestorer:
    def __init__(self):
        with open('utils/emojis.json', encoding='utf-8') as j:
            emoji_list = json.load(j)['emojis']

        self.html_to_emoji = {emoji['html']: emoji['emoji'] for emoji in emoji_list if emoji['html'] is not ''}
        self.unicode_to_emoji = {emoji['unicode']: emoji['emoji'] for emoji in emoji_list if emoji['unicode'] is not ''}

    def restore_emoji(self, tweet, html=True, unicode=False):
        if html:
            for k, v in self.html_to_emoji.items():
                tweet = tweet.replace(k, v)
        if unicode:
            for k, v in self.unicode_to_emoji.items():
                tweet = tweet.replace(k, v)
        return tweet
