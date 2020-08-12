import json
import pandas as pd
from collections import defaultdict


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


all_pos = load_json_as_df('2019-09-01-eng-pos_neg_emo-pos.json')
counts_pos, evidence_num_pos = count_evidence(all_pos)

all_neg = load_json_as_df('2019-09-01-eng-pos_neg_emo-neg.json')
counts_neg, evidence_num_neg = count_evidence(all_neg)

