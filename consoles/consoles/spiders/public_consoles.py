import os
import sys

import scrapy
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

sys.path.insert(0, os.path.abspath('..'))
from telegram import send, send_keep_alive

xbox = "https://www.public-cyprus.com.cy/product/gaming/consoles/xbox-series-x/microsoft-xbox-series-x/prod10724537pp/"
ps5digital = "https://www.public-cyprus.com.cy/product/gaming/consoles/ps5/sony-playstation-5-digital-edition/prod10810253pp/"
ps5disc = "https://www.public-cyprus.com.cy/product/gaming/consoles/ps5/sony-playstation-5-konsola-leyko/prod10238545pp/"
ps5ratchet = "https://www.public-cyprus.com.cy/product/gaming/consoles/ps5/sony-playstation-5-and-ratchet-and-clank:-rift-apart-bundle/prod13802366pp/"
ps5spider = "https://www.public-cyprus.com.cy/product/gaming/consoles/ps5/sony-playstation-5-plus-destruction-allstars-plus-marvels-spider-man:-miles-morales/prod13923508pp/"

testProduct = "https://www.public.cy/product/gaming/games/xbox-series-x/xbox-series-game--nba-2k22/1628518"

consoles = [xbox, ps5digital, ps5disc, ps5ratchet, ps5spider]

# send_keep_alive("I'm alive. Public")


class PublicConsolesSpider(scrapy.Spider):
    name = 'public_consoles'
    allowed_domains = ['www.public-cyprus.com.cy']
    start_urls = consoles
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    desired_capabilities = options.to_capabilities()

    def parse(self, response):
        # driver = webdriver.Chrome(desired_capabilities=self.desired_capabilities)
        driver = webdriver.Remote(command_executor='http://127.0.0.1:4444/wd/hub',
                                  desired_capabilities=self.desired_capabilities)
        driver.implicitly_wait(15)
        driver.get(response.url)
        wait = WebDriverWait(driver, 15)
        wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "h1")))
        wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "app-product-availability div[class*='typography']")))
        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//app-product-availability//div[@class="mdc-typography--body2" and text() != ""]')))
        except TimeoutException:
            send('me', "Element waiting error on page " + '\n' + response.url)
            raise Exception('Unable to find text in this element after waiting 10 seconds')

        title = driver.find_element_by_css_selector("h1").text
        availability = driver.find_element_by_css_selector("app-product-availability div[class*='typography']").text
        buy_clickable = driver.find_element_by_xpath("(//span[text()='Αγόρασέ το']/../../button[not(@disabled)])[1]").is_displayed()

        try:

            item = {
                'product_name': title,
                # 'price_range': item[1],
                'availability': availability,
            }
            if item['availability'] != 'εξαντλήθηκε' and item['availability'] != 'προσωρινά εξαντλημένο':
                if buy_clickable:
                    send('chat', "\n".join(item.values()) + '\n' + response.url)
                    send('me', "\n".join(item.values()) + '\n' + response.url)
            driver.quit()
        except:
            send('me', 'I died. Public')
            driver.quit()
