#!/usr/bin/env python
# coding: utf-8

# In[32]:


get_ipython().system('pip install selenium')


# In[28]:


import requests
from bs4 import BeautifulSoup

url = 'https://www.imdb.com/chart/top/?ref_=nv_mv_250'

response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

movie_list = soup.select('td.titleColumn')
movie_links = []

for movie in movie_list:
    link = movie.a['href']
    movie_links.append('https://www.imdb.com' + link)


# In[8]:


print(movie_links[0])


# In[5]:


import numpy as np
import pandas as pd
from scrapy.selector import Selector
from selenium import webdriver 
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from tqdm import tqdm
import warnings
warnings.filterwarnings("ignore")


# In[14]:


driver = webdriver.Chrome('chromedriver.exe')


# In[ ]:


#from selenium import webdriver  #從library中引入webdriver
#driver = webdriver.Chrome('chromedriver.exe')    
#driver = webdriver.Chrome('chromedriver.exe')
url = movie_links[0]+'reviews/?ref_=tt_ov_rt'
time.sleep(1)
driver.get(url)
time.sleep(1)
title = driver.title
print(driver.title)
time.sleep(1)
body = driver.find_element(By.CSS_SELECTOR, 'body')
body.send_keys(Keys.PAGE_DOWN)
time.sleep(1)
body.send_keys(Keys.PAGE_DOWN)
time.sleep(1)
body.send_keys(Keys.PAGE_DOWN)


sel2 = Selector(text = driver.page_source)
review_counts = sel2.css('.lister .header span::text').extract_first().replace(',','').split(' ')[0]
more_review_pages = int(int(review_counts)/25)

for i in tqdm(range(more_review_pages)):
    try:
        css_selector = 'load-more-trigger'
        driver.find_element(By.ID, css_selector).click()
        time.sleep(1.5)
    except:
        pass

rating = sel2.css('.rating-other-user-rating span::text').extract_first()
review = sel2.css('.text.show-more__control::text').extract_first().strip()
review_date = sel2.css('.review-date::text').extract_first().strip()
author = sel2.css('.display-name-link a::text').extract_first().strip()
review_title = sel2.css('a.title::text').extract_first().strip()
review_url = sel2.css('a.title::attr(href)').extract_first().strip()
helpfulness = sel2.css('.actions.text-muted::text').extract_first().strip()
print('nRating:',rating)
print('nreview_title:',review_title)
print('nAuthor:',author)
print('nreview_date:',review_date)
print('nreview:',review)
print('nhelpfulness:',helpfulness)


rating_list = []
review_date_list = []
review_title_list = []
author_list = []
review_list = []
review_url_list = []
error_url_list = []
error_msg_list = []
reviews = driver.find_elements(By.CSS_SELECTOR, 'div.review-container')

for d in tqdm(reviews):
    try:
        sel2 = Selector(text = d.get_attribute('innerHTML'))
        try:
            rating = sel2.css('.rating-other-user-rating span::text').extract_first()
        except:
            rating = np.NaN
        try:
            review = sel2.css('.text.show-more__control::text').extract_first()
        except:
            review = np.NaN
        try:
            review_date = sel2.css('.review-date::text').extract_first()
        except:
            review_date = np.NaN    
        try:
            author = sel2.css('.display-name-link a::text').extract_first()
        except:
            author = np.NaN    
        try:
            review_title = sel2.css('a.title::text').extract_first()
        except:
            review_title = np.NaN
        try:
            review_url = sel2.css('a.title::attr(href)').extract_first()
        except:
            review_url = np.NaN
        rating_list.append(rating.strip('\n'))
        review_date_list.append(review_date.strip('\n'))
        review_title_list.append(review_title.strip('\n'))
        author_list.append(author.strip('\n'))
        review_list.append(review.strip('\n'))
        review_url_list.append(review_url.strip('\n'))
    except Exception as e:
        error_url_list.append(url)
        error_msg_list.append(e)
data = {'Review_Date':review_date_list,
    'Author':author_list,
    'Rating':morating_list,
    'Review_Title':review_title_list,
    'Review':review_list,
    'Review_Url':review_url
    }
review_df = pd.DataFrame.from_dict(data,orient="index").transpose()
driver.quit()


# In[21]:





# In[ ]:


for i in range(250,251): 
    driver = webdriver.Chrome('chromedriver.exe')
    #from selenium import webdriver  #從library中引入webdriver
    #driver = webdriver.Chrome('chromedriver.exe')    
    #driver = webdriver.Chrome('chromedriver.exe')
    url = movie_links[i] +'reviews/?ref_=tt_ov_rt'
    time.sleep(1)
    driver.get(url)
    time.sleep(1)
    title = driver.title
    print(driver.title)
    time.sleep(1)
    body = driver.find_element(By.CSS_SELECTOR, 'body')
    body.send_keys(Keys.PAGE_DOWN)
    time.sleep(1)
    body.send_keys(Keys.PAGE_DOWN)
    time.sleep(1)
    body.send_keys(Keys.PAGE_DOWN)


    sel2 = Selector(text = driver.page_source)
    review_counts = sel2.css('.lister .header span::text').extract_first().replace(',','').split(' ')[0]
    more_review_pages = int(int(review_counts)/25)

    for i in tqdm(range(more_review_pages)):
        try:
            css_selector = 'load-more-trigger'
            driver.find_element(By.ID, css_selector).click()
            time.sleep(1.5)
        except:
            pass

    rating = sel2.css('.rating-other-user-rating span::text').extract_first()
    review = sel2.css('.text.show-more__control::text').extract_first().strip()
    review_date = sel2.css('.review-date::text').extract_first().strip()
    author = sel2.css('.display-name-link a::text').extract_first().strip()
    review_title = sel2.css('a.title::text').extract_first().strip()
    review_url = sel2.css('a.title::attr(href)').extract_first().strip()
    helpfulness = sel2.css('.actions.text-muted::text').extract_first().strip()
    print('nRating:',rating)
    print('nreview_title:',review_title)
    print('nAuthor:',author)
    print('nreview_date:',review_date)
    print('nreview:',review)
    print('nhelpfulness:',helpfulness)


    rating_list = []
    review_date_list = []
    review_title_list = []
    author_list = []
    review_list = []
    review_url_list = []
    error_url_list = []
    error_msg_list = []
    reviews = driver.find_elements(By.CSS_SELECTOR, 'div.review-container')

    for d in tqdm(reviews):
        try:
            sel2 = Selector(text = d.get_attribute('innerHTML'))
            try:
                rating = sel2.css('.rating-other-user-rating span::text').extract_first()
            except:
                rating = np.NaN
            try:
                review = sel2.css('.text.show-more__control::text').extract_first()
            except:
                review = np.NaN
            try:
                review_date = sel2.css('.review-date::text').extract_first()
            except:
                review_date = np.NaN    
            try:
                author = sel2.css('.display-name-link a::text').extract_first()
            except:
                author = np.NaN    
            try:
                review_title = sel2.css('a.title::text').extract_first()
            except:
                review_title = np.NaN
            try:
                review_url = sel2.css('a.title::attr(href)').extract_first()
            except:
                review_url = np.NaN
            rating_list.append(rating.strip('\n'))
            review_date_list.append(review_date.strip('\n'))
            review_title_list.append(review_title.strip('\n'))
            author_list.append(author.strip('\n'))
            review_list.append(review.strip('\n'))
            review_url_list.append(review_url.strip('\n'))
        except Exception as e:
            error_url_list.append(url)
            error_msg_list.append(e)
    data = {'Review_Date':review_date_list,
        'Author':author_list,
        'Rating':rating_list,
        'Review_Title':review_title_list,
        'Review':review_list,
        'Review_Url':review_url
        }
    review_df = pd.DataFrame.from_dict(data,orient="index").transpose()
    driver.quit()

    title.split('-')[0]
    file_name = 'top_250/'+ title.split('-')[0]+'.csv'
    review_df.to_csv(file_name,index_label = False)


# In[ ]:




