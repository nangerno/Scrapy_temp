import scrapy
from scrapy import signals
from scrapy.http import HtmlResponse
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

class MySpider(scrapy.Spider):
    name = 'my_spider'
    start_urls = ['https://spothero.com/search?kind=city&id=32&view=dl']  # Replace with the URL you want to scrape

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(MySpider, cls).from_crawler(crawler, *args, **kwargs)
        crawler.signals.connect(spider.spider_closed, signal=signals.spider_closed)
        return spider

    def spider_closed(self):
        self.driver.quit()

    def parse(self, response):
        # Use Selenium to interact with the page and wait for the content to load
        options = Options()
        options.headless = False
        # service = Service('C:/Program Files/Google/Chrome/Application/chrome.exe')  # Replace with the path to your chromedriver executable
        self.driver = webdriver.Chrome(service=None, options=options)
        self.driver.get(response.url)
        
        # Wait for the page to fully load (you may need to adjust the waiting time)
        self.driver.implicitly_wait(10)

        # Extract the JSON-LD content using Selenium
        element = self.driver.find_element(By.XPATH, '//script[@type="application/ld+json"]')
        json_ld_content = element.get_attribute('innerHTML')
        print("json_ld_content")
        if json_ld_content:
            # Process the extracted JSON-LD content as needed
            print(json_ld_content)

        # Close the Selenium driver
        self.driver.quit()
    