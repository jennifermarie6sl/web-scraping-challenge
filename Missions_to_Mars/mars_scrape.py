# Import Dependencies
from splinter import Browser 
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import time
import requests
from time import sleep
import pandas as pd
import pymongo

mars_data = {}

def scrape_info():
    executable_path = {'executable_path': '/Users/jenniferrocha/.wdm/drivers/chromedriver/mac64/94.0.4606.41/chromedriver'}
    browser = Browser('chrome', **executable_path, headless=False)
    
    # Visit Mars site
    url = "https://mars.nasa.gov/news"
    browser.visit(url)
    browser.is_element_present_by_css('div.list_text', wait_time=1)

    # Scrape page into Soup
    html = browser.html
    html_soup = soup(html, "html.parser")

    article = html_soup.select_one('div.list_text') #select one grabs the first instance
    news_title = article.find('div', class_="content_title").get_text()
    news_p = article.find('div', class_="article_teaser_body").get_text()
    
    mars_data = {
        "title": news_title,
        "content": news_p
    }
    time.sleep(2)

#     print(mars_data)
    

#     Visit JPL to get image
    jpl_url = "https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html"
    browser.visit(jpl_url)

    # Scrape page into Soup
    image_html = browser.html
    image_soup = soup(image_html, "html.parser")
    
    open_btn = image_soup.find()
    image = image_soup.find('img', class_= 'headerimage fade-in')['src']
    build = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/'
    full_image_url = build + image

    mars_data.update({"image_url": full_image_url})
    time.sleep(2)


    # Visit Mars Facts to get facts
    facts_url = "https://space-facts.com/mars/"
    browser.visit(facts_url)
    
     # Scrape page into Soup   
    page = requests.get(facts_url)
    facts_soup = soup(page.text, 'html.parser')
    dfs = pd.read_html(page.text)
    df= pd.DataFrame(dfs[0])
    facts_for_html = df.to_html(header=False, index = False)

    # print(facts_for_html)
    
    mars_data.update({'facts': facts_for_html})
    
    print(mars_data)

    time.sleep(2)


    # Visit Hemisphere to get Pics and Titles   
    hem_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(hem_url)

    hemisphere_image_urls = [] 
    
    for i in range(4):
        hemisphere = {}
        browser.find_by_css("a.product-item h3")[i].click()
        time.sleep(1)
        html = browser.html
        hemi_soup = soup(html, "html.parser")
        hemisphere['img_url'] = hemi_soup.find("a", text="Sample").get("href")
        hemisphere['title'] = hemi_soup.find("h2", class_="title").get_text()
        hemisphere_image_urls.append(hemisphere)
        browser.back()
    
    print(hemisphere_image_urls)

    mars_data.update({'hem_urls': hemisphere_image_urls})

    browser.quit()
    return mars_data

# scrape_info()




