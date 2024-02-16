#!/usr/bin/env python3

import json
import time

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

MSSC_URL = 'https://mason.my.site.com/SelfServiceHC/s/'


def scrape_topic(driver, url):
    driver.get(url)
    # All of the JavaScript on the page needs a few seconds to load; wait until
    # at least one 'article-link' element has been loaded
    delay = 10
    try:
        myElem = WebDriverWait(driver, delay).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'article-link')))
    except TimeoutException:
        print('Loading took too much time!')
        driver.close()
        exit(1)
    needToLoadMore = True
    while needToLoadMore:
        buttons = driver.find_elements(By.CLASS_NAME, 'loadmore')
        # as long as the 'loadmore' button exists, click it and then wait for
        # more links to load into the page
        if len(buttons) > 0:
            buttons[0].click()
            # wait for the new links to load before trying again
            time.sleep(3)
        else:
            needToLoadMore = False

    articles = driver.find_elements(By.CLASS_NAME, 'article-link')
    articleUrls = []
    for article in articles:
        articleUrls.append(article.get_attribute('href'))
    return articleUrls


def scrape_article(driver, url):
    results = {}
    results['url'] = url
    driver.get(url)
    # All of the JavaScript on the page needs a few seconds to load
    time.sleep(3)
    divs = driver.find_elements(By.TAG_NAME, 'div')
    for div in divs:
        if div.get_attribute('data-target-selection-name') == 'sfdc:RecordField.Knowledge__kav.Question__c':
            results['question'] = div.get_attribute('innerText').strip()
        elif div.get_attribute('data-target-selection-name') == 'sfdc:RecordField.Knowledge__kav.Answer__c':
            results['answer'] = div.get_attribute('innerText').strip()
    # TODO: 1) tags, 2) last-modified-date
    # last-modified-data is <span class=uiOutputDate ...>Jan 5, 2024</span>
    return results


if __name__ == '__main__':
    driver = webdriver.Chrome()
    driver.get(MSSC_URL)
    # All of the JavaScript on the page needs a few seconds to load; wait until
    # at least one 'topicLink' element has been loaded
    try:
        myElem = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'topicLink')))
    except TimeoutException:
        print('Loading took too much time!')
        driver.close()
        exit(1)
    topics = driver.find_elements(By.CLASS_NAME, 'topicLink')
    topicUrls = []
    for topic in topics:
        topicUrl = topic.get_attribute('href')
        topicUrls.append(topicUrl)
    articleUrls = []
    for url in topicUrls:
        urls = scrape_topic(driver, url)
        articleUrls.extend(urls)
    results = []
    for url in articleUrls:
        result = scrape_article(driver, url)
        # print(json.dumps(result))
        results.extend(result)
    print(json.dumps(results))
    driver.close()
