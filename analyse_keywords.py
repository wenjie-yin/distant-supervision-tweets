import json
import pandas as pd
from collections import defaultdict
from methods import KeywordCriterion
from utils.keywords import positive_negative


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
    return pd.Series(counts), pd.Series(evidence_numbers)


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
    all_pos = load_json_as_df('2019-09-01-eng-pos_neg_emo-pos.json')
    counts_pos, evidence_num_pos = count_evidence(all_pos)

    all_neg = load_json_as_df('2019-09-01-eng-pos_neg_emo-neg.json')
    counts_neg, evidence_num_neg = count_evidence(all_neg)

    founta_df = pd.read_csv("~/Projects/stage0/data/founta_mode_basic_3classes.csv")
    davidson_df = pd.read_csv("~/Projects/stage0/data/davidson_mode_basic.csv")

    criterion = KeywordCriterion(positive_negative)

    founta_overlap = category_annotation_overlap(founta_df, criterion)
    davidson_overlap = category_annotation_overlap(davidson_df, criterion)
    # get indexes e.g. overlap.groups[('neg', 2)]

    overlap_proportion(founta_overlap, founta_df)
    overlap_proportion(davidson_overlap, davidson_df)
