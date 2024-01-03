import streamlit as st
from modules.facebook import FacebookCrawler


cookie = st.text_input("Cookie")
url = st.text_input("URL to crawl")
type = st.selectbox("Type", ["", "Group", "Page"])
pages = st.number_input("Pages to crawl", 1, 10, 5)


if cookie != "" and url != "" and type != "":
    crawler = FacebookCrawler()
    crawler.go(url, cookie=cookie)
    posts = crawler.crawl(int(pages))
    st.dataframe(posts)
