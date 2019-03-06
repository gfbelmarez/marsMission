#!/usr/bin/env python
# coding: utf-8

import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
from splinter.browser import Browser


# #### Mars News

def getMarsNews():
    NASA_link = "https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"
    response = requests.get(NASA_link)
    soup = bs(response.text)
    latest_news = soup.find_all("div", class_='slide')[0]
    headline = latest_news.find("div", class_='content_title').text.strip()
    paragraph = latest_news.find("div", class_='rollover_description_inner').text.strip()
    news = {'headline': headline, 'paragraph': paragraph}
    return news
    
# #### Mars Image

def getMarsFeaturedImage():
    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    browser = Browser('chrome', **executable_path)
    image_site = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(image_site)
    link = browser.find_by_id('full_image').first['data-fancybox-href']
    featured_image_url = image_site + link
    return featured_image_url


# #### Mars Weather

def getMarsWeather():
    mars_twitter = "https://twitter.com/marswxreport?lang=en"
    response = requests.get(mars_twitter)
    soup = bs(response.text)
    latest_tweet = soup.find_all("div", class_="content")[0]
    p = latest_tweet.find("p", class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text")
    mars_weather = p.text.strip()
    return mars_weather


# #### Mars Facts

def getMarsFacts():
    mars_facts_site = "https://space-facts.com/mars/"
    response = requests.get(mars_facts_site)
    soup = bs(response.text)
    table = soup.find("table", id="tablepress-mars")
    mars_facts = pd.read_html(str(table))
    return mars_facts


# #### Mars Hemispheres

def getMarsHemispheres():
    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    browser = Browser('chrome', **executable_path)
    image_site = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(image_site)
    hemisphere_image_urls = []
    for item in browser.find_by_css('div[class="description"]'):
        title = item.find_by_css('h3').text
        link = item.find_by_css('a')['href']
        new_links = {'title':title, 'url': link}
        hemisphere_image_urls.append(new_links)
    return hemisphere_image_urls


def scrape():
    marsData = {}
    marsData['news'] = getMarsNews()
    marsData['featured_image'] = getMarsFeaturedImage()
    marsData['weather'] = getMarsWeather()
    marsData['facts'] = getMarsFacts()
    marsData['hemispheres'] = getMarsHemispheres()
    return marsData




