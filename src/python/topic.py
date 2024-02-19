#!/usr/bin/env python3

import time

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def get_articles_from_topic(driver, topicUrl):
    driver.get(topicUrl)
    articleUrls = []
    # All of the JavaScript on the page needs a few seconds to load; wait until
    # at least one 'article-link' element has been loaded
    try:
        myElem = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'article-link')))
    except TimeoutException:
        return articleUrls
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
    for article in articles:
        articleUrls.append(article.get_attribute('href'))
    return articleUrls
