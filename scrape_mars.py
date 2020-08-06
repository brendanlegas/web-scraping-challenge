#import dependencies
from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd



def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    return Browser("chrome", **executable_path, headless=True)

def scrape_info():
    browser = init_browser()

    #NASA Mars News
    url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")

    container = soup.find("div", class_="image_and_description_container")
    news_title = container.find("div", class_="content_title").text
    news_p = soup.find("div",class_="article_teaser_body").text


    #Mars Facts
    url = 'https://space-facts.com/mars/'
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")

    table = soup.find("table")
    dfs = pd.read_html(str(table))
    df = dfs[0]

    mars_data = {
        "news_title": news_title,
        "news_p": news_p,
        "table": df
    }

    browser.quit()

    print(mars_data)

    return mars_data

scrape_info()