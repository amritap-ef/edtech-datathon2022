import pandas as pd
import re

def _process_vocab(v):
    v = v.split("\n\n")
    v = [re.split("[/,]", voc.split(":")[-1]) for voc in v]
    v = [phrase.strip() for phrases in v for phrase in phrases]
    v = [phrase for phrase in v if phrase not in ["", "etc."]]
    return v

def process_data(fpath="data/obs_topics_id.json", fpath_to_save="data/obs_topics_id_processed.csv"):
    df = pd.read_json(fpath).T
    df = pd.concat([df, df["lesson_learning_context"].apply(pd.Series)], axis=1)
    df["Vocabulary"] = df["Vocabulary"].apply(_process_vocab)
    df.to_csv(fpath_to_save)

if __name__ == "__main__":
    process_data()