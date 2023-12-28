from pandas import DataFrame, Index
import streamlit as st
from modules.sentiment import SentimentAnalysis

sa = SentimentAnalysis()

messages = st.text_area("Chat message")
items = [(message, *sa.predict(message)) for message in messages.split("\n")]

df = DataFrame(items, columns=["Message", "Level", "Weight"])
st.dataframe(df, use_container_width=True)
