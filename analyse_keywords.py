import json
import pandas as pd
from collections import defaultdict
from methods import KeywordCriterion, GroupCriterion
from utils.keywords import *
import pickle
import glob
import re


def load_json_as_df(filename):
    all_dicts = []
    with open(filename) as f:
        for line in f:
            all_dicts.append(json.loads(line.strip()))
    return pd.DataFrame(all_dicts)


def count_evidence(df):
    counts = defaultdict(int)
    evidence_numbers = defaultdict(int)
    for _, row in df.iterrows():
        for evidence in row['evidence']:
            counts[evidence] += 1
        evidence_numbers[len(row['evidence'])] += 1
    return pd.Series(counts).sort_values(ascending=False), pd.Series(evidence_numbers).sort_values(ascending=False)


def category_annotation_overlap(dataset_df, criterion):
    hits = dataset_df.apply(lambda x: criterion.categorise(x['tweet']),
                           axis=1, result_type='expand')
    dataset_df = pd.concat([dataset_df, hits], axis=1).rename(columns={0: 'category', 1: 'evidence'})

    return dataset_df.groupby(['category', 'class'])


def overlap_proportion(overlap, dataset_df):
    counts = overlap.size().reset_index().rename(columns={0: 'counts'})
    proportion = counts.apply(lambda x: x['counts'] / dataset_df['class'].value_counts()[x['class']], axis=1)
    counts['proportion'] = proportion
    return counts


if __name__ == "__main__":

    founta_df = pd.read_csv("~/Projects/stage0/data/founta_mode_basic_3classes.csv")
    davidson_df = pd.read_csv("~/Projects/stage0/data/davidson_mode_basic.csv")

    criterion = KeywordCriterion(positive_negative)

    founta_overlap = category_annotation_overlap(founta_df, criterion)
    davidson_overlap = category_annotation_overlap(davidson_df, criterion)
    # get indexes e.g. overlap.groups[('neg', 2)]

    overlap_proportion(founta_overlap, founta_df)
    overlap_proportion(davidson_overlap, davidson_df)

    '''
    all_pos = load_json_as_df('2019-09-01-eng-pos_neg_emo-pos.json')
    counts_pos, evidence_num_pos = count_evidence(all_pos)

    all_neg = load_json_as_df('2019-09-01-eng-pos_neg_emo-neg.json')
    counts_neg, evidence_num_neg = count_evidence(all_neg)

    '''

    with open('all_counts.pkl', 'rb') as f:
        all_counts = pickle.load(f)

    o_files = glob.glob("semeval-tweets-2013-2017/semeval_official/GOLD/Subtask_A/twitter-*.txt")
    df_list = list()
    for file in o_files:
        df = pd.read_table(file, header=None, names=['tweet_id', 'label', 'text'], index_col=False)
        set_name = file.split('/')[-1].split('-')[1]
        name_split = re.split(r'([0-9]+)([a-z]+)', set_name)
        df['year'] = name_split[1]
        df['split'] = name_split[2]
        df_list.append(df)
    all_semeval = pd.concat(df_list).rename(columns={'text': 'tweet', 'label': 'class'})

    train_semeval = all_semeval[all_semeval['split'] == 'train']

    emoji_criterion = KeywordCriterion(emojis, name='emojis')
    emoticon_criterion = KeywordCriterion(emoticons, consider_surrounding=True, name='emoticons')
    emoji_emoticon_criterion = GroupCriterion([emoticon_criterion, emoji_criterion], name="emoji_emoticon")

    semeval_overlap = category_annotation_overlap(train_semeval, emoji_emoticon_criterion)
    overlap_proportion(semeval_overlap, train_semeval)

    count_evidence(semeval_overlap.get_group(('neg', 'positive')))

    for year in ['2013', '2015', '2016']:
        single_year_df = train_semeval[train_semeval['year'] == year]
        single_year_overlap = category_annotation_overlap(single_year_df, emoji_emoticon_criterion)
        print(year + '\n')
        print(overlap_proportion(single_year_overlap, single_year_df))

