import os
import sys
from urllib.parse import urlparse

import scrapy
from lxml.doctestcompare import strip

sys.path.insert(0, os.path.abspath('..'))
from telegram import send, send_keep_alive

ps5digital = "https://www.electroline.com.cy/products/computing/gaming130/gaming-consoles13022/sony-playstation-5-digital-version-white/"
ps5disc = "https://www.electroline.com.cy/products/computing/gaming130/gaming-consoles13022/sony-playstation-5-disc-version-white/"

testProduct = "https://www.electroline.com.cy/products/computing/gaming130/accessories13022/sony-playstation-5-hd-camera-white/"

consoles = [ps5digital, ps5disc]

send_keep_alive("I'm alive. Electroline")


class ElectrolineConsolesSpider(scrapy.Spider):
    name = 'electroline_consoles'
    allowed_domains = ['www.electroline.com.cy']
    start_urls = consoles

    def parse(self, response):
        try:
            product_name = response.css('.single-product-title::text').extract()
            price_range = response.css('h2.product-price--single::text').extract()
            availability_online = response.css('.c-product-availability-icon-group--online > span::text').extract()
            availability_stores = response.css('.c-product-availability-icon-group--in-stores > span::text').extract()

            row_data = zip(product_name, price_range, availability_online, availability_stores)

            for item in row_data:
                scraped_info = {
                    'product_name': item[0],
                    'price_range': strip(item[1]),
                    'availability_online': 'Not available online' if strip(
                        item[2]) == 'Mη διαθέσιμο για αποστολή' else "Available online",
                    'availability_stores': 'Not available in stores' if strip(
                        item[3]) == 'Mη διαθέσιμο στα καταστήματα' else "Available in stores",
                }

                if scraped_info['availability_online'] != 'Not available online' \
                        or scraped_info['availability_stores'] != 'Not available in stores':
                    send('me', "\n".join(scraped_info.values()) + '\n' + response.url)
                    send('chat', "\n".join(scraped_info.values()) + '\n' + response.url)
        except:
            send('me', 'I died. Electroline')
