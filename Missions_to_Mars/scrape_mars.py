# ----
# # Mission to Mars
# ----
# Author: Felipe Murillo
# Created: June 13, 2020
# Description: Build a web application that scrapes various websites for data related to the Mission to Mars and displays the information in a single HTML page
# ----

# Configure dependencies
from bs4 import BeautifulSoup as bs
from splinter import Browser
import os
import time
import re
import pandas as pd

def scrape():

    # Setup Google ChromeDriver (for Mac)
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}

    # Launch a Google chrome browser
    browser = Browser("chrome", **executable_path, headless=False)

    #### NASA Mars News

    # Browse NASA Mars News Site
    browser.visit("https://mars.nasa.gov/news/")

    # Wait 3 seconds for NASA page to laod before converting soup
    time.sleep(3)

    # Convert HTML into a Beautiful Soup
    nasaNewsHTML = browser.html
    soup = bs(nasaNewsHTML,"html.parser")

    # Pull the latest headlines
    # Note the title class is used for website title as well, need to take the 2nd element of content_title
    news_title = soup.find_all("div",class_="content_title", limit=2)[1].text
    news_p = soup.find("div",class_="article_teaser_body").text

    # Print results
    print(f"{news_title}")
    print(f"------------")
    print(f"{news_p}")


    #### JPL Mars Space Images

    # Browse JPL Space Images website
    jplImages = "https://www.jpl.nasa.gov"
    browser.visit(f"{jplImages}/spaceimages/?search=&category=Mars")

    # Convert HTML into a Beautiful Soup
    jplHTML = browser.html
    soup = bs(jplHTML,"html.parser")

    # Pull URL data from soup pointing to the featured MARS image
    bgImage = soup.find("article",class_="carousel_item").get('style')

    # Extract local URL
    URL = bgImage.split("'")[1]

    # Now, construct the explicit featured image URL
    featured_image_url = jplImages + URL

    # Print Image URL
    print(featured_image_url)


    #### Mars Weather

    # Browse @MarsWxReport Twitter Account
    marsTwitter = "https://twitter.com/marswxreport?lang=en"
    browser.visit(marsTwitter)

    # Wait 5 seconds for NASA page to laod before converting soup
    time.sleep(5)

    # Convert HTML into a Beautiful Soup
    twitter = browser.html
    soup = bs(twitter,"lxml")

    # Grab the latest mars weather update from twitter (without using class names they they are dynamic)
    InSight = soup.find(text=re.compile('InSight sol'))

    # Format the weather entry and save
    mars_weather = InSight.replace('InSight sol', 'Sol', 1)

    # Print results
    print(mars_weather)


    #### Mars Facts

    # Browse Mars Facts website
    marsFacts = "https://space-facts.com/mars/"

    # Read all tabels contained in URL
    tables = pd.read_html(marsFacts)

    # Obtained desired table (1st one) and export as HTML
    factTable = tables[0].set_index(0)

    # Export table as HTML (ithout header and index name)
    factTable.to_html(os.path.join(".","templates/fact_table.html"), header=False, index_names = False)


    ##### Mars Hemispheres

    # Browse Mars Astrogeology page for hemispheric images
    marsHemis = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(marsHemis)

    # Convert HTML into a Beautiful Soup
    hemis = browser.html
    soup = bs(hemis,"lxml")

    # Pull links to hemisphere pages
    results = soup.find_all("a", class_="itemLink product-item")

    # Create a list of unique weblinks
    hemiLinks = []
    for item in results:
        if item.get('href') not in hemiLinks:
            hemiLinks.append(item.get('href'))

    # Close browser once data is pulled
    browser.quit()
    
    # USGS URL is required to complete URL
    usgs_url = 'https://astrogeology.usgs.gov'

    # Initialize list
    hemisphere_image_urls = []

    for link in hemiLinks:
        hemisphere_dict = {}
        
        # Initialize browser
        browser = Browser("chrome", **executable_path, headless=False)
        
        # Visit specific hemisphere weblink
        browser.visit(usgs_url+link)
        hemi_i = browser.html
        
        # Create soup of html
        soup = bs(hemi_i,"lxml")
        
        # Collect hemisphere name and url for representative image
        hemisphere_dict['title'] = soup.find('h2',class_="title").text.replace(' Enhanced','')
        hemisphere_dict['img_url'] = soup.find('div', class_='downloads').a.get('href')
        
        # Add hemisphere dictionary to list
        hemisphere_image_urls.append(hemisphere_dict)
        
        # Close browser once data is pulled
        browser.quit()

    # Print results
    print(hemisphere_image_urls)

    # Construct results dictionary
    results = {
        'news_title' : news_title,
        'news_p': news_p,
        'featured_image_url': featured_image_url,
        'mars_weather' : mars_weather,
        'hemisphere_image_urls': hemisphere_image_urls
    }

    return results