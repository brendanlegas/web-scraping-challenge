#import dependencies
from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd
import time


def scrape_info():
    mars_dict = {}

    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    browser = Browser("chrome", **executable_path, headless=True, user_agent='Chrome/84.0.4147.105')

    #NASA Mars News
    url1 = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
    browser.visit(url1)
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")

    container = soup.find("div", class_="image_and_description_container")
    news_title = container.find("div", class_="content_title").text
    news_p = soup.find("div",class_="article_teaser_body").text

    mars_dict['news_title']=news_title
    mars_dict['news_p']=news_p

    #Mars image
    url_2='https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'

    browser.visit(url_2)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    #click the full image button
    click1=browser.find_by_css('a[class="button fancybox"]').click()
    ##click1=browser.links.find_by_partial_text('FULL IMAGE').click()

    #click the more info button
    click2=browser.links.find_by_partial_text('more info').click()

    #parse the page
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    #find the link to the full size image
    img_partial = soup.find_all('img',class_='main_image')[0]['src']

    featured_img_url = f'https://www.jpl.nasa.gov{img_partial}'
    
    mars_dict['featured_img_url']=featured_img_url
    featured_img_url

    #Mars Facts
    url3 = 'https://space-facts.com/mars/'
    browser.visit(url3)
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")

    table = soup.find("table")
    dfs = pd.read_html(str(table))
    df = dfs[0]
    df = df.rename(columns = {0: 'Planet Profile', 1:''})
    df = df.set_index('Planet Profile', drop=True)

    df.to_html('mars_html')
    
    mars_dict['mars_facts']=df.to_html(justify='left')

    #Twitter Feed

    url4 = 'https://twitter.com/MarsWxReport?lang=en'

    browser.visit(url4)
    time.sleep(2)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    tweet_search = soup.find_all('article')
    mars_weather=tweet_search[0].find_all('span')[4].text

    mars_dict['mars_weather']=mars_weather

    #Hemispheres
    base_url = 'https://astrogeology.usgs.gov/'
    #Mars Hemispheres Cerberus
    hemisphere_image_urls = []
    url5 = 'https://astrogeology.usgs.gov/search/map/Mars/Viking/cerberus_enhanced'
    browser.visit(url5)
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")

    images = soup.find_all("img", class_='wide-image')
    title = soup.find("h2", class_="title").text
    for image in images:
        link_cerberus = image['src']
    ceberus_dict = {
        "title": title, "img_url": base_url + link_cerberus
    }
    hemisphere_image_urls.append(ceberus_dict)

    #Mars Hemispheres Schiaparelli
    url6 = 'https://astrogeology.usgs.gov/search/map/Mars/Viking/schiaparelli_enhanced'
    browser.visit(url6)
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")

    images = soup.find_all("img", class_='wide-image')
    title = soup.find("h2", class_="title").text
    for image in images:
        link_schiaparelli = image['src']
    schiaparelli_dict = {
        "title": title, "img_url": base_url + link_schiaparelli
    }
    hemisphere_image_urls.append(schiaparelli_dict)

    #Mars Hemispheres Syrtis Major Hemisphere
    url7 = 'https://astrogeology.usgs.gov/search/map/Mars/Viking/syrtis_major_enhanced'
    browser.visit(url7)
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")

    images = soup.find_all("img", class_='wide-image')
    title = soup.find("h2", class_="title").text
    for image in images:
        link_syrtis = image['src']
    syrtis_dict = {
        "title": title, "img_url": base_url + link_syrtis
    }
    hemisphere_image_urls.append(syrtis_dict)

    #MArs Hemispheres Valles Marineris
    url8 = 'https://astrogeology.usgs.gov/search/map/Mars/Viking/valles_marineris_enhanced'
    browser.visit(url8)
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")

    images = soup.find_all("img", class_='wide-image')
    title = soup.find("h2", class_="title").text
    for image in images:
        link_valles = image['src']
    valles_dict = {
        "title": title, "img_url": base_url + link_valles
    }
    hemisphere_image_urls.append(valles_dict)

    mars_dict['hemisphere_image_urls'] = hemisphere_image_urls

    browser.quit()
    print(mars_dict)

    return mars_dict

#scrape_info()