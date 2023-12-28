import streamlit as st
from modules.sentiment import SentimentAnalysis

sa = SentimentAnalysis()
text = st.text_input("Text to analyze")

level, weight = sa.predict(text)
color = ""
match level:
    case "Positive":
        color = "green"
    case "Negative":
        color = "red"
    case "Neutral":
        color = "gray"

st.markdown(
    f"""
<div style="margin: 0 auto; padding: 12px; text-align: center">
    <div style="font-size: 24px; font-weight: bold; margin-bottom: 12px; color: {color}">
        {level}
    </div>
    <div style="font-size: 16px; font-weight: bold">
        {round(weight * 100, 2)}%
    </div>
</div>
    """,
    unsafe_allow_html=True
)
