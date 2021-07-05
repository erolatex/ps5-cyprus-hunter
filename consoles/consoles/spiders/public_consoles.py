import os
import sys

import scrapy
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

sys.path.insert(0, os.path.abspath('..'))
from telegram import send, send_keep_alive

xbox = "https://www.public-cyprus.com.cy/product/gaming/consoles/xbox-series-x/microsoft-xbox-series-x/prod10724537pp/"
ps5digital = "https://www.public-cyprus.com.cy/product/gaming/consoles/ps5/sony-playstation-5-digital-edition/prod10810253pp/"
ps5disc = "https://www.public-cyprus.com.cy/product/gaming/consoles/ps5/sony-playstation-5-konsola-leyko/prod10238545pp/"
ps5ratchet = "https://www.public-cyprus.com.cy/product/gaming/consoles/ps5/sony-playstation-5-and-ratchet-and-clank:-rift-apart-bundle/prod13802366pp/"

testProduct = "https://www.public-cyprus.com.cy/product/tileorasi-samsung-qled-85-4k-qe85q60t/prod10634466pp/"

consoles = [xbox, ps5digital, ps5disc, ps5ratchet]


class PublicConsolesSpider(scrapy.Spider):
    name = 'public_consoles'
    allowed_domains = ['www.public-cyprus.com.cy']
    start_urls = consoles
    options = webdriver.ChromeOptions()
    # options.add_argument("--headless")
    desired_capabilities = options.to_capabilities()

    def parse(self, response):
        send_keep_alive("I'm alive. Public")
        driver = webdriver.Chrome(desired_capabilities=self.desired_capabilities)
        driver.implicitly_wait(10)
        driver.get(response.url)
        wait = WebDriverWait(driver, 10)
        wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".product-title")))
        wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".soldbypublic")))

        title = driver.find_element_by_css_selector(".product-title").text
        availability = driver.find_element_by_css_selector(".soldbypublic").text
        try:

            item = {
                'product_name': title,
                # 'price_range': item[1],
                'availability': availability,
                'url': response.url,
            }
            if item['availability'] != 'εξαντλήθηκε!':
                send('chat', "\n".join(item.values()) + '\n' + response.url)
                send('me', "\n".join(item.values()) + '\n' + response.url)
        except:
            send('me', 'I\'m died. Public')
