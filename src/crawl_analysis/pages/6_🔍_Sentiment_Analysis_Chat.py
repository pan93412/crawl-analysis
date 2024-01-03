from pandas import DataFrame
import streamlit as st
from modules.sentiment import SentimentAnalysis

st.set_page_config(page_title="Sentiment Analysis: Chat/Comments", page_icon="🔍")

sa = SentimentAnalysis()

messages = st.text_area("Chat message")
items = [(message, *sa.predict(message)) for message in messages.split("\n")]

df = DataFrame(items, columns=["Message", "Level", "Weight"])
st.dataframe(df, use_container_width=True)
