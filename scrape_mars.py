from splinter import Browser
from bs4 import BeautifulSoup


def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)


def scrape():
    browser = init_browser()
    news = {}

    news_url = "https://mars.nasa.gov/news/"
    browser.visit(news_url)

    news_html = browser.html
    news_soup = BeautifulSoup(news_html, "html.parser")

    news_html = news_soup.find('div', class_= 'slide')
    news["title"] = news_html .find("div", class_="content_title").get_text().strip('\n')
    news["p"] = news_html.find("div", class_="rollover_description").get_text().strip('\n')

    jpl_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(jpl_url)

    jpl = {}

    jpl_html = browser.html
    jpl_soup = BeautifulSoup(jpl_html, "html.parser")

    jpl_html = (str(jpl_soup.find('article', class_= 'carousel_item')).split("background-image: url('/")[1]).split("')")[0]
    jpl["ft_img_url"] = f'https://www.jpl.nasa.gov/{jpl_html}'

    return news, jpl

if __name__ == "__main__":
    print(scrape())


# def scrape():
#     browser = init_browser()
#     listings = {}

#     url = "https://raleigh.craigslist.org/search/hhh?max_price=1500&availabilityMode=0"
#     browser.visit(url)

#     html = browser.html
#     soup = BeautifulSoup(html, "html.parser")

#     listings["headline"] = soup.find("a", class_="result-title").get_text()
#     listings["price"] = soup.find("span", class_="result-price").get_text()
#     listings["hood"] = soup.find("span", class_="result-hood").get_text()

#     return listings

