import streamlit as st
from modules.line import LineCrawler

print("LOADING, wait.")

lc = LineCrawler()

# text
st.button("Open LINE", on_click=lambda: lc.open_line())
group_name = st.text_input("Group name")
if st.button("Search group"):
    result = lc.search_group(group_name)
    st.text_area("Content", result, height=200)
