from pandas import DataFrame, Index
import streamlit as st
import torch
from modules.keyword_extractor import KeywordExtractor

ke = KeywordExtractor(torch.device("mps"))

messages = st.text_area("Chat message")
if messages != "":
    items = ke.split_words_raw([message for message in messages.split("\n") if message != ""])
    st.write(list(items))
