#!/usr/bin/env python3

import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

MSSC_URL = 'https://mason.my.site.com/SelfServiceHC/s/'

def scrape_topic(driver, url):
    print('Scraping', url)
    driver.get(url)
    # All of the JavaScript on the page needs a few seconds to load; wait until 
    # at least one 'article-link' element has been loaded
    delay = 10
    try:
        myElem = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.CLASS_NAME, 'article-link')))
        print('Page is ready')
    except TimeoutException:
        print('Loading took too much time!')
        driver.close()
        exit(1)

    needToLoadMore = True
    while(needToLoadMore):
        buttons = driver.find_elements(By.CLASS_NAME, 'loadmore')
        # as long as the 'loadmore' button exists, click it and then wait for 
        # more links to load into the page
        if len(buttons) > 0:
            buttons[0].click()
            #wait for the new links to load before trying again
            time.sleep(3)
        else:
            needToLoadMore = False

    articles = driver.find_elements(By.CLASS_NAME, 'article-link')
    articleUrls = []
    for article in articles:
        articleUrls.append(article.get_attribute('href'))
    return articleUrls

def scrape_article(driver, url):
    print('Scraping article', url)
    driver.get(url)
    # All of the JavaScript on the page needs a few seconds to load
    time.sleep(3)
    divs = driver.find_elements(By.CLASS_NAME, 'uiOutputRichText')

    # TODO: Find 1) question, 2) answer, 3) tags, 4) last-modified-date

    print(len(divs))

if __name__ == '__main__':
    # TODO: Local ChromeDriver
    driver = webdriver.Chrome()
    # TODO: Remote web driver with Selenium Grid is an option
    #options = webdriver.ChromeOptions()
    #driver = webdriver.Remote(command_executor='http://localhost:4444', options=options)

    print('Getting root URL')
    driver.get(MSSC_URL)

    # All of the JavaScript on the page needs a few seconds to load; wait until 
    # at least one 'topicLink' element has been loaded
    delay = 10
    try:
        myElem = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.CLASS_NAME, 'topicLink')))
        print('Page is ready')
    except TimeoutException:
        print('Loading took too much time!')
        driver.close()
        exit(1)

    topics = driver.find_elements(By.CLASS_NAME, 'topicLink')
    print(len(topics), "topics found on the main page")
    topicUrls = []
    for topic in topics:
        topicUrl = topic.get_attribute('href')
        topicUrls.append(topicUrl)

    articleUrls = []
    for url in topicUrls:
        urls = scrape_topic(driver, url)
        print(len(urls))
        articleUrls.extend(urls)
        print(len(articleUrls))

    for url in articleUrls:
        scrape_article(driver, url)

    print("Done scraping")
    driver.close()
