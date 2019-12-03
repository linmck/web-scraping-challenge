from splinter import Browser
from bs4 import BeautifulSoup


def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)


def scrape():
    nasa_mars_news_browser = init_browser()
    story = {}

    nasa_mars_news_url = "https://mars.nasa.gov/news/"
    nasa_mars_news_browser.visit(nasa_mars_news_url)

    nasa_mars_html = browser.html
    news_soup = BeautifulSoup(nasa_mars_html, "html.parser")

    story["title"] = news_soup.find("div", class_="content_title").get_text()
    story["p"] = news_soup.find("div", class_="rollover_description").get_text()

    jpl_browser = init_browser()
    story = {}

    jpl_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    jpl_browser.visit(jpl_url)

    jpl_html = 


    return story


