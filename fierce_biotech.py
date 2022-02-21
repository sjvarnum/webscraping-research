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
url = 'https://www.fiercebiotech.com/'
driver = webdriver.Firefox(service=service, options=options)
wait = WebDriverWait(driver, 10)

driver.get(url)
sleep(5)

# body = driver.page_source
# html = HTML(html=body)

see_more_link = driver.find_element(By.LINK_TEXT, 'See more articles')
driver.execute_script('arguments[0].scrollIntoView(true);', see_more_link)
sleep(5)

for n in range(100):
    try:
        close_button = driver.find_element(
            By.CSS_SELECTOR, '.close-persistent-bar').click()
        sleep(5)
        driver.find_element(By.LINK_TEXT, 'See more articles').click()
    except:
        driver.find_element(By.LINK_TEXT, 'See more articles').click()

    sleep(5)
    see_more_link = driver.find_element(By.LINK_TEXT, 'See more articles')
    driver.execute_script('arguments[0].scrollIntoView(true);', see_more_link)
    see_more_link.click()
    sleep(5)
    n = random.randint(1, 5)
    sleep(n)


body = driver.page_source
html = HTML(html=body)
articles = html.find('article.node-listing.prosumer.row')
article_list = []
for article in articles:
    try:
        title = article.find('.element-title.small', first=True).text
        print(title)
    except:
        None
    try:
        # link = base_url + article.find('.article-title', first=True).links.pop()
        link = url[:-1] + article.find('.element-title.small > a', first=True).links.pop()
        print(link)
    except:
        None
    try:
        date = article.find('span.date.d-inline-block', first=True).text
        date = datetime.strptime(date[:-2], '%b %d, %Y %H:%M').strftime('%Y-%m-%d')
        print(date)
    except:
        None
    try:
        channel = article.find(
            '.label.label-small > span > a', first=True).text
        print(channel)
    except:
        None

    data = {
            'date': date,
            'source': 'fiercebiotech',
            'channel': channel,
            'title': title,
            'link': link
        }
    
    article_list.append(data)

driver.close()

df = pd.DataFrame(article_list)
# df['date'] = pd.to_datetime(df['date']).dt.strftime('%Y-%m-%d')
df = df[['date', 'source', 'channel', 'title', 'link']]
df.drop_duplicates(inplace=True)
datestamp = datetime.today().strftime('%Y%m%dT%H%M')
df.to_csv(f'Fierce_Biotech_{datestamp}.csv', index=None)
