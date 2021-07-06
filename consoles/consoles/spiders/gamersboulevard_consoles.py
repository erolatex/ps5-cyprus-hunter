import os
import sys

import scrapy
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

sys.path.insert(0, os.path.abspath('..'))
from telegram import send, send_keep_alive

xbox = "https://www.gamersboulevard.com/products/details?name=Xbox%20Series%20X%20Console"
ps5digital = "https://www.gamersboulevard.com/products/details?name=PlayStation%205%20Digital"
ps5disc = "https://www.gamersboulevard.com/products/details?name=PlayStation%205"

testProduct = "https://www.gamersboulevard.com/products/details?name=G.I.%20Joe%20Retro%20Collection%20Series%20Duke%20Action%20Figure%2010%20cm%202021"

consoles = [xbox, ps5digital, ps5disc, testProduct]


# send_keep_alive("I'm alive. Gamersboulevard")


class GamersboulevardConsolesSpider(scrapy.Spider):
    name = 'gamersboulevard_consoles'
    allowed_domains = ['www.gamersboulevard.com']
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
        # wait = WebDriverWait(driver, 10)
        # wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".product-title")))
        # wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".product-price > span")))
        # wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "h2 > strong")))

        title = driver.find_element_by_css_selector(".product-title").text
        price = driver.find_element_by_css_selector(".product-price > span").text
        availability = driver.find_element_by_css_selector("h2 > strong").text
        try:

            item = {
                'product_name': title,
                'price_range': price,
                'availability': availability,
            }
            if item['availability'] != 'Out of Stock':
                send('chat', "\n".join(item.values()) + '\n' + response.url)
                send('me', "\n".join(item.values()) + '\n' + response.url)
            driver.quit()
        except:
            send('me', 'I died. Gamersboulevard')
            driver.quit()
