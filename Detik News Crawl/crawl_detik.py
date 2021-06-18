from bs4 import BeautifulSoup
import pandas as pd
import json, random, re, requests
from datetime import datetime
import seaborn as sns

class Detik_Crawler():
    def __init__(self, topic):
        self.topic = topic

    def get_urls(self):
        urls = []
        news_links = []
        page = 1
        # get news URL from page 1 to 10
        while True:
            url = f"https://www.detik.com/search/searchall?query={self.topic}&siteid=2&sortby=time&page={page}"
            html_page = requests.get(url).content
            soup = BeautifulSoup(html_page, 'lxml')
            articles = soup.find_all('article')
            
            if not articles: # if there's no articles left
                break

            for article in articles:
                urls = article.find_all('a')
                for url in urls:
                    news_links.append(url.get('href'))
            
            page += 1
                    
        return news_links


    def extract_news(self):
        # get news article details from scraped urls
        scraped_info = []
        url_list = self.get_urls()
        for news in self.get_urls():
            source = news
            html_page = requests.get(news).content
            soup = BeautifulSoup(html_page, 'lxml')
            # check if title, author, date, news div, is not None type
            title = soup.find('h1', class_='detail__title')
            if title is not None:
                title = title.text
                title = title.replace('\n', '')
                title = title.strip()

            date = soup.find('div', class_='detail__date')
            if date is not None:
                date = date.text

            news_div = soup.find_all('div', class_='detail__body-text itp_bodycontent')
            if news_div is not None:
                for news in news_div:
                    news_content_list = news.find_all('p')
                    news_content_list = [content.text for content in news_content_list]
                    news_content = ' '.join(news_content_list)
                    # convert scraped data into dictionary
                    news_data = {
                        "url": source,
                        "judul": title,
                        "tanggal": date,
                        "isi": news_content
                    }
                    # add dicts into a list
                    scraped_info.append(news_data)

        df = pd.DataFrame.from_dict(scraped_info)
        df.to_csv(f'scrap_results/detik_{self.topic}.csv',index=False)

if __name__ == '__main__':
    crawler_obj = Detik_Crawler('pajak sembako')
    crawler_obj.extract_news()
    