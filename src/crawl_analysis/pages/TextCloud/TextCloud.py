from wordcloud import WordCloud, STOPWORDS
from pandas import DataFrame, Index
import streamlit as st
import torch
from modules.keyword_extractor import KeywordExtractor
import matplotlib.pyplot as plt

ke = KeywordExtractor(torch.device("mps"))

messages = st.text_area("Chat message")
if messages != "":
    items = ke.split_words([message for message in messages.split("\n") if message != ""])
    l = list(items)

    freq = {w: l.count(w) for w in set(l)}

    p, ax = plt.subplots()
    ax.imshow(WordCloud(background_color="white", contour_width=3, contour_color='steelblue', font_path="/Users/pan93412/Library/Fonts/NotoSansTC[wght].ttf").generate_from_frequencies(freq))
    st.pyplot(p)
