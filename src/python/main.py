#!/usr/bin/env python3

import json

from selenium import webdriver
from article import scrape_article
from catalog import get_topics_from_catalog
from topic import get_articles_from_topic


if __name__ == '__main__':
    driver = webdriver.Chrome()
    topicUrls = get_topics_from_catalog(driver)
    articleUrls = []
    for url in topicUrls:
        articles = get_articles_from_topic(driver,  url)
        for article in articles:
            if article not in articleUrls:
                articleUrls.append(article)
    results = []
    for url in articleUrls:
        result = scrape_article(driver, url)
        print(json.dumps(result))
        results.extend(result)
