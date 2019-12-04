from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd
import pymongo


def init_browser():
    # Chrome driver path
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)

def scrape():

    conn = "mongodb://localhost:27017"
    client = pymongo.MongoClient(conn)
    db = client.mars_db

    browser = init_browser()

# Nasa news scrape
    news_url = "https://mars.nasa.gov/news/"
    browser.visit(news_url)

    news = {}

    news_html = browser.html
    news_soup = BeautifulSoup(news_html, "html.parser")
    news_html = news_soup.find('div', class_= 'slide')

    news["title"] = news_html .find("div", class_="content_title").get_text().strip('\n')
    news["p"] = news_html.find("div", class_="rollover_description").get_text().strip('\n')
    
    news_collection = db['mars_news']
    db.news_collection.insert_many(news)
    
    # JPL scrape
    jpl_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(jpl_url)

    jpl = {}

    jpl_html = browser.html
    jpl_soup = BeautifulSoup(jpl_html, "html.parser")
    jpl_html = (str(jpl_soup.find('article', class_= 'carousel_item')).split("background-image: url('/")[1]).split("')")[0]
    jpl["ft_img_url"] = f'https://www.jpl.nasa.gov/{jpl_html}'

    jpl_collection = db['mars_jpl']
    db.jpl_collection.insert_many(jpl)
    
    # Twitter scrape
    twitter_url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(twitter_url)

    tweet = {}

    twitter_html = browser.html
    twitter_soup = BeautifulSoup(twitter_html, "html.parser")
    twitter_html = twitter_soup.find('div', class_= 'original-tweet')
    tweet["weather"] = (twitter_html.find('p', class_='tweet-text').get_text().split('pic')[0]).strip('\n')

    twitter_collection = db['mars_tweet']
    db.twitter_collection.insert_many(tweet)

    # Mars facts scrape
    facts_url = 'https://space-facts.com/mars/'
    browser.visit(facts_url)

    facts = []

    facts_html = browser.html
    facts_soup = BeautifulSoup(facts_html, "html.parser")
    facts_html = facts_soup.find("table", class_= "tablepress")
    facts_out = facts_html.find_all("tr")

    for row in facts_out:
        category = row.find("td", class_="column-1").get_text()
        value = row.find("td", class_="column-2").get_text()
        
        fact = {
            "category": category,
            "value": value
        }
        facts.append(fact)

    facts_collection = db['mars_facts']
    db.facts_collection.insert_many(facts)

    # Hemisphere scrape
    hemisphere_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(hemisphere_url)

    products_html = browser.html
    products_soup = BeautifulSoup(products_html, "html.parser")

    products = products_soup.find_all('div', class_= 'item')

    hemisphere_urls = []

    for product in products:
        title = product.find('h3').get_text()
        link = product.find('a')
        link = link.attrs['href']
        
        hemisphere = {
            'title': title,
            'link': f'https://astrogeology.usgs.gov{link}'
        }
        
        hemisphere_urls.append(hemisphere)

    hemisphere_collection = db['mars_hemisphere_urls']
    db.hemisphere_collection.insert_many(hemisphere_urls)

    # Return results of all scrapes
    return news, jpl, tweet, facts, hemisphere_urls

if __name__ == "__main__":
    print(scrape())
    print("Data Uploaded!")
