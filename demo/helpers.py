import ast
import pandas as pd
import streamlit as st
import urllib

@st.experimental_memo(show_spinner=False)
def load_obs_topics_data(fpath="data/obs_topics_id.json"):
    df = pd.read_csv(fpath)
    df["Vocabulary"] = df["Vocabulary"].apply(ast.literal_eval)
    df["Stage"] = df["Stage"].apply(lambda s: s.lower().strip())
    return df

def get_url_caption_youtube(url, start):
    params = {'t': start}
    url_caption = url + '&' + urllib.parse.urlencode(params)
    return url_caption