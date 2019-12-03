from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd


def init_browser():
    # Chrome driver path
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)


def scrape():
    # Nasa news scrape
    browser = init_browser()
    news = {}

    news_url = "https://mars.nasa.gov/news/"
    browser.visit(news_url)

    news_html = browser.html
    news_soup = BeautifulSoup(news_html, "html.parser")

    news_html = news_soup.find('div', class_= 'slide')
    news["title"] = news_html .find("div", class_="content_title").get_text().strip('\n')
    news["p"] = news_html.find("div", class_="rollover_description").get_text().strip('\n')

    # JPL scrape
    jpl_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(jpl_url)

    jpl = {}

    jpl_html = browser.html
    jpl_soup = BeautifulSoup(jpl_html, "html.parser")

    jpl_html = (str(jpl_soup.find('article', class_= 'carousel_item')).split("background-image: url('/")[1]).split("')")[0]
    jpl["ft_img_url"] = f'https://www.jpl.nasa.gov/{jpl_html}'
    
    # Twitter scrape
    twitter_url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(twitter_url)

    tweet = {}

    twitter_html = browser.html
    twitter_soup = BeautifulSoup(twitter_html, "html.parser")

    twitter_html = twitter_soup.find('div', class_= 'original-tweet')
    tweet["weather"] = (twitter_html.find('p', class_='tweet-text').get_text().split('pic')[0]).strip('\n')

    # Mars facts scrape
    facts_url = 'https://space-facts.com/mars/'
    browser.visit(facts_url)

    facts = {}

    facts_html = browser.html
    facts_soup = BeautifulSoup(facts_html, "html.parser")

    facts_html = str(facts_soup.find('table', class_= 'tablepress'))
    facts["table"] = pd.read_html(facts_html)

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

    # Return results of all scrapes
    return news, jpl, tweet, facts, hemisphere_urls

if __name__ == "__main__":
    print(scrape())
