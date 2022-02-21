from datetime import datetime
import pandas as pd
import random
from requests_html import HTML
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.service import Service
from selenium.common.exceptions import *
from time import sleep

service = Service('geckodriver.exe')
options = webdriver.FirefoxOptions()
# options.add_argument('-headless')
base_url = 'https://www.beckershospitalreview.com'
driver = webdriver.Firefox(service=service, options=options)
wait = WebDriverWait(driver, 10)

pages = range(0, 20, 20)
urls = []
for page in pages:
    url = f'https://www.beckershospitalreview.com/?start={page}'
    urls.append(url)

article_list = []
for url in urls:
    driver.get(url)
    body = driver.page_source
    html = HTML(html=body)

    articles = html.find('.article')

    for article in articles:
        try:
            title = article.find('.article-title', first=True).text
        except:
            None
        try:
            link = base_url + \
                article.find('.article-title', first=True).links.pop()
        except:
            None
        try:
            date = article.find('.article-date > time', first=True)
            date = date.attrs['datetime']
            date = date.split('T')[0]
        except:
            None
        try:
            channel = link.split('/')[3]
        except:
            None

        data = {
            'date': date,
            'source': 'www.beckershospitalreview.com',
            'channel': channel,
            'title': title,
            'link': link
        }

        article_list.append(data)

        n = random.randint(1, 5)
        sleep(n)

driver.close()

df = pd.DataFrame(article_list)
df['date'] = pd.to_datetime(df['date']).dt.strftime('%Y-%m-%d')
df = df[['date', 'source', 'channel', 'title', 'link']]
df.drop_duplicates(inplace=True)
datestamp = datetime.today().strftime('%Y%m%dT%H%M')
df.to_csv(f'Beckers_Hospital_Review_Articles_{datestamp}.csv', index=None)
