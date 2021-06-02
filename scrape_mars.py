import os
from bs4 import BeautifulSoup as bs
import requests
from splinter import Browser
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd

def init_browser():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    return Browser("chrome", **executable_path, headless=False)


def scrape():
    
    browser = init_browser()
    
    MarsDict = {}

    url = "https://mars.nasa.gov/news/"
    response = requests.get(url)
    soup = bs(response.text, 'html.parser')

    news_title = soup.find_all('div', class_='content_title')[0]
    news_text = soup.find_all('div', class_='rollover_description_inner')[0]
    
    MarsDict['news_title'] = news_title.get_text()
    MarsDict['news_text'] = news_text.get_text()

    jpl_url = "https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html"

    browser.visit(jpl_url)
    html = browser.html
    soup = bs(html,'html.parser')

    image = soup.find('img', class_='headerimage fade-in')

    base_url = "https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/"

    featured_image_url = base_url + image['src']

    MarsDict['featured_image_url'] = featured_image_url

    mars_facts_url = "https://space-facts.com/mars/"

    tables = pd.read_html(mars_facts_url)
    df = tables[0]
    df.rename(columns = {1:'Mars Statistics', 2:' '})
    df.to_html('MarsFacts.html')
    
    usgs_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(usgs_url)
    html = browser.html
    soup = bs(html,'html.parser')

    items = soup.find_all('div', class_='item')

    hemisphere_image_urls = []

    usgs_base_url = 'https://astrogeology.usgs.gov'

    for item in items:
        title = item.find('h3').text
        image_url = item.find('a', class_='itemLink product-item')['href']
        browser.visit(usgs_base_url + image_url)
        image_html = browser.html
        soup = bs(image_html, 'html.parser')
        image_url = usgs_base_url + soup.find('img', class_='wide-image')['src']
        hemisphere_image_urls.append({'Title': title, "Image_URL": image_url})

    MarsDict['hemisphere_image_urls'] = hemisphere_image_urls

    # Quit the browser
    browser.quit()

    return MarsDict




