import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd
from datetime import datetime

def get_last_date(df):
    dates =pd.to_datetime(df['Date']).apply(lambda x: int(x.timestamp() * 1000))
    dates =sorted(dates.tolist(), reverse=True)
    return dates[0]



"""
NEWS DATA FROM ESG TODAY
"""

def scrape_esg_today(last_date):

    titles=[]
    categories=[]
    times=[]
    authors=[]
    headline_texts=[]
    #465
    for i in range(1,10000):

        print(f'SCRAPPED {i} PAGE')

        driver = webdriver.ChromiumEdge()

        # Navigate to a website
        url = f'https://www.esgtoday.com/category/esg-news/page/{i}/'
        driver.get(url)

        time.sleep(2)

        categories_page=driver.find_elements('class name', 'post-category')
        things = driver.find_elements('tag name', 'h2')[:10]
        authors_page=driver.find_elements('class name', 'author-name')
        times_page = driver.find_elements('tag name', 'time')
        list_titles=[el.text for el in things]
        list_categories=[el.text for el in categories_page]
        list_times=[el.text for el in times_page]
        date_object = datetime.strptime(list_times[0], "%B %d, %Y")
        date_milliseconds = int(date_object.timestamp()) * 1000
        if date_milliseconds<=last_date:
            break
        else:
            print(f"DATE_LAST:{last_date} \nDATE_HERE:{date_milliseconds}:{list_times[0]}")
        list_authors=[el.text for el in authors_page]
        inner_texts=[]
        inner_links=[]
        for headline in things:
            inner_links.append(headline.find_element('tag name','a').get_attribute('href'))


        # print(inner_links)
        for inner_link in inner_links:
            driver.get(inner_link)
            inner_text=driver.find_element('class name','entry-content').text
            inner_texts.append(inner_text)
            time.sleep(1)
            # driver.quit()

        driver.get(url)
        # time.sleep(2)



        titles.extend(list_titles)
        headline_texts.extend(inner_texts)
        categories.extend(list_categories)
        times.extend(list_times)
        authors.extend(list_authors)
        driver.quit()



    data = []

    for i in range(0, len(times)):
      item = {}
      item['Date'] = times[i]
      item['Title'] = titles[i]
      item['Text']=headline_texts[i]
      item['Category'] = categories[i]
      item['site'] = "ESGTODAY"
      data.append(item)

    esgToday = pd.DataFrame(data)

    return esgToday


def scrape_to_date(df):
    last_date=get_last_date(df)
    return scrape_esg_today(last_date)