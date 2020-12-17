# Use MongoDB with Flask templating to create a new HTML page that displays all of the information that was scraped from the URLs above.

# * Start by converting your Jupyter notebook into a Python script called `scrape_mars.py` with a function called `scrape` that will execute all of your scraping code from above and return one Python dictionary containing all of the scraped data.

# * Next, create a route called `/scrape` that will import your `scrape_mars.py` script and call your `scrape` function.

#   * Store the return value in Mongo as a Python dictionary.

# * Create a root route `/` that will query your Mongo database and pass the mars data into an HTML template to display the data.

# * Create a template HTML file called `index.html` that will take the mars data dictionary and display all of the data in the appropriate HTML elements. Use the following as a guide for what the final product should look like, but feel free to create your own design.


import pandas as pd
from bs4 import BeautifulSoup as bs
from splinter import Browser
import os

mars_data = {}
def init_browser():
    executable_path = {'executable_path': 'chromedriver.exe'}
    return Browser('chrome', **executable_path, headless=False)
    

def scrape():
    mars = {}
    browser = init_browser()
    
    # Mars News Scrape
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    html = browser.html
    soup = bs(html, 'html.parser')
    news_title = soup.find_all('div', class_='content_title')[0].text
    news_p = soup.find_all('div', class_='article_teaser_body')[0].text
  

   
    # JPL IMG Scrape
    jpl_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(jpl_url)
    html = browser.html
    jpl_soup = bs(html, 'html.parser')
    image_path = jpl_soup.find_all('img')[3]["src"]
    jpl_url_short = 'https://www.jpl.nasa.gov'
    featured_image_url = jpl_url_short + image_path
    

    
    # Facts Scrape
    facts_url = 'https://space-facts.com/mars/'
    mars_facts = pd.read_html(facts_url)
    mars_facts_df = mars_facts[2]
    mars_facts_df.columns = ["Description", "Value"]
    mars_facts_html = mars_facts_df.to_html()
    

    

    # Hemi Scrape
    hemi_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(hemi_url)
    html = browser.html
    hemi_soup = bs(html, 'html.parser')
    hemisphere_image_urls = []
    mars_hemispheres = hemi_soup.find('div', class_='collapsible results')
    mars_hemispheres_items = mars_hemispheres.find_all('div', class_='item')



    for i in mars_hemispheres_items:
        hemisphere = i.find('div', class_="description")
        title = hemisphere.h3.text
        each_hemi_url = hemisphere.a["href"]    
        browser.visit('https://astrogeology.usgs.gov' + each_hemi_url)
        each_hemi_image_html = browser.html
        each_hemi_image_soup = bs(each_hemi_image_html, 'html.parser')
        each_hemi_image_link = each_hemi_image_soup.find('div', class_='downloads')
        each_hemi_image_url = each_hemi_image_link.find('li').a['href']
        image_dict = {}
        image_dict['title'] = title
        image_dict['img_url'] = each_hemi_image_url
        hemisphere_image_urls.append(image_dict)

    
    mars = {
        "news_title": news_title,
        "paragraph": news_p,
        "image": featured_image_url,
        "facts": mars_facts_html,
        "hemisphere": hemisphere_image_urls
    }

    browser.quit()

    return mars