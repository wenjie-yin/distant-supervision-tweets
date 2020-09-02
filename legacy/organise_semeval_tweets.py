import pandas as pd
import glob

all_semeval = []
a_files = glob.glob('semeval-tweets-2013-2017/*.txt')
for file in a_files:
    all_semeval.append(pd.read_table(file, header=None, names=['tweet_id', 'label', 'text']).set_index('tweet_id'))
all_semeval_df = pd.concat(all_semeval, axis=0)

o_files = glob.glob("semeval-tweets-2013-2017/semeval_official/DOWNLOAD/Subtask_A/*.txt")
found_list = list()
not_found_list = list()
for file in o_files:

    df = pd.read_table(file, header=None, names=['tweet_id', 'label'], index_col=False)
    set_name = file.split('/')[-1].split('-')[1]
    try:
        found = df[df.apply(lambda row: row['tweet_id'] in all_semeval_df.index, axis=1)]
        found.loc[:, 'text'] = found.apply(lambda row: all_semeval_df.text.loc[row['tweet_id']], axis=1)
        found.loc[:, 'set_name'] = set_name
        found_list.append(found)

        try:
            not_found = df[~df.tweet_id.isin(found.tweet_id)].copy()
            not_found.loc[:, 'set_name'] = set_name
            not_found_list.append(not_found)
        except ValueError:
            continue
    except:
        print(set_name)

all_not_found = pd.concat(not_found_list)
all_found = pd.concat(found_list)
