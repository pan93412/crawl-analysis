import streamlit as st
from models.database import TypedDatabase
from modules.facebook import FacebookCrawler

st.set_page_config(page_title="Crawlers: Facebook", page_icon="🐜")
database = TypedDatabase()

cookie = st.text_input("Cookie")
url = st.text_input("URL to crawl")
type = st.selectbox("Type", ["", "Group", "Page"])
pages = st.number_input("Pages to crawl", 1, 10, 5)
headless = st.checkbox("Headless", value=False)


if st.button("Start crawling"):
    crawler = FacebookCrawler(database.facebook_post_model(), headless=headless)
    crawler.go(url, cookie=cookie if cookie != "" else None)
    posts = crawler.crawl(int(pages))
    st.dataframe(posts)
