#!/usr/bin/env python3

import json
import time

from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By


def scrape_article(driver, url):
    results = {}
    results['url'] = url
    results['tags'] = []
    driver.get(url)
    # All of the JavaScript on the page needs a few seconds to load
    time.sleep(3)
    divs = driver.find_elements(By.TAG_NAME, 'div')
    for div in divs:
        if div.get_attribute('data-target-selection-name') == \
                'sfdc:RecordField.Knowledge__kav.Question__c':
            results['question'] = div.get_attribute('innerText').strip()
        elif div.get_attribute('data-target-selection-name') == \
                'sfdc:RecordField.Knowledge__kav.Answer__c':
            results['answer'] = div.get_attribute('innerText').strip()
    results['date'] = driver.find_element(By.CLASS_NAME, 'date')\
        .get_attribute('innerText').strip()
    tagList = driver.find_elements(By.CLASS_NAME, 'slds-pill')
    for tag in tagList:
        results['tags'].append(tag.get_attribute('innerText'))
    return results


if __name__ == '__main__':
    driver = webdriver.Chrome()
    # this is a sample article URL for testing
    result = scrape_article(driver, 'https://mason.my.site.com/SelfServiceHC/s/article/Degree-From-Unaccredited-Institution')
    print(json.dumps(result))
