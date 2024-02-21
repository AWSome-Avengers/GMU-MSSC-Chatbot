#!/usr/bin/env python3

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


TOPIC_CATALOG_URL = 'https://mason.my.site.com/SelfServiceHC/s/topiccatalog'


def get_topics_from_catalog(driver):
    driver.get(TOPIC_CATALOG_URL)
    # All of the JavaScript on the page needs a few seconds to load; wait until
    # at least one 'topicHierarchy-top' element has been loaded
    try:
        myElem = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME,
                                            'topicHierarchy-top')))
    except TimeoutException:
        print('Loading catalog took too much time!')
        driver.close()
        exit(1)
    topicUrls = []
    topics = driver.find_elements(By.CLASS_NAME, 'topicHierarchy-top')
    topics.extend(driver.find_elements(By.CLASS_NAME, 'topicHierarchy-child'))
    topics.extend(driver.find_elements(By.CLASS_NAME,
                                       'topicHierarchy-grandChild'))
    for topic in topics:
        topicUrls.append(topic.get_attribute('href'))
    return topicUrls


if __name__ == '__main__':
    driver = webdriver.Chrome()
    topicUrls = get_topics_from_catalog(driver)
