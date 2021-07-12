import os
import sys

import scrapy
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

sys.path.insert(0, os.path.abspath('..'))
from telegram import send, send_keep_alive

xbox = "https://www.stephanis.com.cy/en/products/gaming/gaming-consoles/xbox/367294"
ps5digital = "https://www.stephanis.com.cy/en/products/gaming/gaming-consoles/playstation/367339"
ps5disc = "https://www.stephanis.com.cy/en/products/gaming/gaming-consoles/playstation/367338"

testProduct = "https://www.stephanis.com.cy/en/products/gaming/gaming-consoles/playstation/367258"

consoles = [xbox, ps5digital, ps5disc, testProduct]


# send_keep_alive("I'm alive. Stephanis")


class StephanisConsolesSpider(scrapy.Spider):
    name = 'stephanis_consoles'
    allowed_domains = ['www.stephanis.com.cy']
    start_urls = consoles
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    desired_capabilities = options.to_capabilities()

    def parse(self, response):
        # driver = webdriver.Chrome(desired_capabilities=self.desired_capabilities)
        driver = webdriver.Remote(command_executor='http://127.0.0.1:4444/wd/hub',
                                  desired_capabilities=self.desired_capabilities)
        driver.implicitly_wait(10)
        driver.get(response.url)
        wait = WebDriverWait(driver, 10)
        wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".product-title")))
        wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".item-price")))
        # wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "h2 > strong")))

        title = driver.find_element_by_css_selector(".product-title").text
        price = driver.find_element_by_css_selector(".item-price").text
        availability = not driver.find_element_by_css_selector("#OutOfStockContainer").is_displayed()

        try:

            item = {
                'product_name': title,
                'price_range': price,
            }
            if availability:
                item['availability'] = 'Available'
                send('me', "\n".join(item.values()) + '\n' + response.url)
                send('chat', "\n".join(item.values()) + '\n' + response.url)
            driver.quit()
        except:
            send('me', 'I died. Stephanis')
            driver.quit()
