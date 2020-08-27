# Import Dependencies
from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd
import requests
import pymongo

def home():
    executable_path = {"executable_path": "chromedriver.exe"}
    return Browser("chrome", **executable_path, headless=False)

def scrape():
    browser = home()
    # create the scrape news dict to insert in mongoDB
    mars_dict ={}

    #run the first function

    latest_title, latest_paragraph = scrape_news()

    # Run all functions and store output in a dictionary
    mars_dict["title"] = latest_title
    mars_dict["paragraph"] = latest_paragraph
    mars_dict["main_image"] = scrape_mars_images()
    mars_dict["mars_facts"] = mars_facts()
    mars_dict["mars_hemispheres"] = mars_hemis()

    browser.quit()

    return mars_dict

    

#Function to screape mars news
def scrape_news():

    browser = home()
    
    nasa_url = 'https://mars.nasa.gov/news/'
    browser.visit(nasa_url)
    html = browser.html
    nasa_soup = BeautifulSoup(html, 'html.parser')

    # get the most up to date news title and paragraph
    try:
        latest_title = nasa_soup.find_all('div', class_='content_title')[1].text
        latest_paragraph = nasa_soup.find_all('div', class_='article_teaser_body')[0].text

    # scrape mars image
    except AttributeError:
        return None, None
    
    browser.quit()

    return latest_title, latest_paragraph
    
    
def scrape_mars_images():

    browser = home()

    
    jpl_url = 'https://www.jpl.nasa.gov'
    nasa_images_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(nasa_images_url)
    html = browser.html
    nasa_images_soup = BeautifulSoup(html, 'html.parser')
    # get featured image link
    image_path = nasa_images_soup.find_all('img')[3]["src"]
    featured_image_url = jpl_url + image_path

    browser.quit()

    return featured_image_url

def mars_facts():
    browser = home()
    # scrape for Mars facts, converted into html table
    mars_facts_url = 'https://space-facts.com/mars/'
    data = pd.read_html(mars_facts_url)
    mars_data = data[2]
    mars_data.columns = ["Description", "Value"]
    mars_html = mars_data.to_html()
    mars_html.replace('\n', '')

    browser.quit()

    return mars_html


def mars_hemis():

    browser = home()   

    Astrogeology_url = 'https://astrogeology.usgs.gov'
    mars_hemispheres_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'

    browser.visit(mars_hemispheres_url)
    mars_hemispheres_url = browser.html
    mars_hemispheres_soup = BeautifulSoup(mars_hemispheres_url, 'html.parser')

    hemispheres = mars_hemispheres_soup.find_all('div', class_='item')

    # create empty dictionary to hold info
    mars_hemisphere_image_urls = []

    for hemis in hemispheres:
        title =hemis.find('h3').text
    
        #store the image
        temp_img = hemis.find('a', class_='itemLink product-item')['href']
    
        #visit it
        browser.visit(Astrogeology_url + temp_img)
    
        temp_img_html = browser.html
    
    
        soup_each_hemis = BeautifulSoup(temp_img_html, 'html.parser')
    
        full_img_url = Astrogeology_url + soup_each_hemis.find('img', class_='wide-image')['src']
    
        mars_hemisphere_image_urls.append({"title": title, "image_url": full_img_url})


    browser.quit()

    return mars_hemisphere_image_urls