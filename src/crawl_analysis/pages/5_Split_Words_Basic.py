import streamlit as st
import torch
from modules.keyword_extractor import KeywordExtractor

st.set_page_config(page_title="WordCloud inside: Split Words", page_icon="🔍")

ke = KeywordExtractor(torch.device("mps"))

messages = st.text_area("Chat message")
if messages != "":
    items = ke.split_words_raw([message for message in messages.split("\n") if message != ""])
    st.write(list(items))
