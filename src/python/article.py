#!/usr/bin/env python3

import time

from selenium.webdriver.common.by import By


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
