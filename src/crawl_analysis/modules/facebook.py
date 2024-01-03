import time
import pandas as pd
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

class FacebookCrawler:
    def __init__(self):
        options = webdriver.ChromeOptions()
        # options.add_argument("--headless=new")

        service = Service(ChromeDriverManager().install())

        # 建立 Selenium 瀏覽器
        self.driver = webdriver.Chrome(service=service, options=options)


    def go(self, url: str, cookie: str|None = None):
        self.driver.get(url)

        if cookie is not None:  # [key]=[value]; [key]=[value]; ...
            cookie_entries = cookie.split("; ")
            for cookie_entry in cookie_entries:
                key, value = cookie_entry.split("=", maxsplit=2)
                self.driver.add_cookie({"name": key, "value": value, 'path': '/'})
            self.driver.refresh()

        # if cookie is not None:
        #     self.driver.execute_script("document.cookie = arguments[0]", cookie)
        #     self.driver.refresh()

        # close the log in window
        for _ in range(5):
            try:
                close_button = self.driver.find_element(By.XPATH, "//div[@aria-label='關閉']")
                close_button.click()
                break
            except NoSuchElementException:
                time.sleep(0.5)


    def crawl(self, pages: int) -> pd.DataFrame:
        df = pd.DataFrame(index=["content", "likes_count", "url"])
        index = ["content", "likes_count", "url"]
        dataset = []

        article_class_name = "x9f619 x1n2onr6 x1ja2u2z x2bj2ny x1qpq9i9 xdney7k xu5ydu1 xt3gfkd xh8yej3 x6ikm8r x10wlt62 xquyuld"
        article_css_selector = "."+".".join(article_class_name.split(" "))
        post_url_class_name = "x1i10hfl xjbqb8w x6umtig x1b1mbwd xaqea5y xav7gou x9f619 x1ypdohk xt0psk2 xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x16tdsg8 x1hl2dhg xggy1nq x1a2a7pz x1heor9g xt0b8zv xo1l8bm"
        post_url_css_selector = "a."+".".join(post_url_class_name.split(" "))

        # Pages to crawl.
        for i in range(pages):
            articles = self.driver.find_elements(
                By.CSS_SELECTOR,
                article_css_selector,
            )

            for article in articles:
                try:
                    post_link_element = article.find_element(By.CSS_SELECTOR, post_url_css_selector)
                except (NoSuchElementException, StaleElementReferenceException):
                    # print("found a post without URL: ", article)
                    continue

                post_url = post_link_element.get_attribute("href")
                if post_url is None:
                    # print("found a post without URL: ", article)
                    continue

                # Remove tracker from URL to prevent duplicate crawling.
                post_url = post_url.split("?")[0]

                # Find a button with '查看更多', and click it.
                # If there's no such button, we don't need to click it.
                try:
                    more_button = article.find_element(
                        By.XPATH,
                        ".//div[.='查看更多']"
                    )
                    if more_button is not None:
                        self.driver.execute_script("arguments[0].click()", more_button)
                except NoSuchElementException:
                    pass

                # Extract the content here.
                try:
                    content_class_name = "x193iq5w xeuugli x13faqbe x1vvkbs xlh3980 xvmahel x1n0sxbx x1lliihq x1s928wv xhkezso x1gmr53x x1cpjm7i x1fgarty x1943h6x x4zkp8e x3x7a5m x6prxxf xvq8zen xo1l8bm xzsf02u x1yc453h"
                    content_div = article.find_element(
                        By.CSS_SELECTOR,
                        "."+".".join(content_class_name.split(" ")),
                    )
                    content = content_div.text
                except NoSuchElementException:
                    content = ""

                if content == "":
                    continue

                # Extract the likes count here.
                try:
                    likes_count_element = article.find_element(
                        By.CSS_SELECTOR,
                        "span.xrbpyxo.x6ikm8r.x10wlt62.xlyipyv.x1exxlbk > span > span",
                    )
                except NoSuchElementException:
                    likes_count_element = None

                # print(likes_count_element, "its text", likes_count_element.text if likes_count_element is not None else None)

                if likes_count_element is not None:
                    like_text = likes_count_element.text.strip()  # 移除空格
                    like_text = like_text.replace(',', '')  # 移除逗號
                else:
                    like_text = ""

                if like_text != "":
                    if '萬' in like_text:
                        # 處理出現 ' 萬' 的數值
                        like = int(float(like_text[:like_text.find('萬')].strip())*10000)
                    else:
                        # 處理有出現 ',' 的數值
                        like = int(like_text.replace(',',''))
                else:
                    like = 0

                dataset.append(pd.Series([content, like, post_url], index=index))

            # Scroll down to get more posts
            self.driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
            # Wait 3 seconds. You can change this number to match the speed of your internet.
            time.sleep(2)


        df = pd.DataFrame(dataset, columns=index)
        # dudup
        df.drop_duplicates(subset=["url"], inplace=True)
        return df
