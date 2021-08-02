import os
import sys
import time

import scrapy
from lxml.doctestcompare import strip

sys.path.insert(0, os.path.abspath('..'))
from telegram import send, send_keep_alive

ps5digital = "https://www.kotsovolos.cy/ProductDisplay?top_category5=&top_category4=&top_category3=&urlRequestType=Base&categoryId=354502&catalogId=10551&top_category2=&productId=8642016&errorViewName=ProductDisplayErrorView&urlLangId=-24&langId=-24&top_category=35012&parent_category_rn=354501&storeId=10161"
ps5disc = "https://www.kotsovolos.cy/ProductDisplay?top_category5=&top_category4=&top_category3=&urlRequestType=Base&categoryId=354502&catalogId=10551&top_category2=&productId=8642026&errorViewName=ProductDisplayErrorView&urlLangId=-24&langId=-24&top_category=35012&parent_category_rn=354501&storeId=10161"
ps5ratchet = "https://www.kotsovolos.cy/ProductDisplay?top_category5=&top_category4=&top_category3=&urlRequestType=Base&categoryId=354502&catalogId=10551&top_category2=&productId=13345005&errorViewName=ProductDisplayErrorView&urlLangId=-24&langId=-24&top_category=35012&parent_category_rn=354501&storeId=10161"

testProduct = "https://www.kotsovolos.cy/ProductDisplay?top_category5=&top_category4=&top_category3=&urlRequestType=Base&categoryId=355501&catalogId=10551&top_category2=&productId=4913002&errorViewName=ProductDisplayErrorView&urlLangId=-24&langId=-24&top_category=35012&parent_category_rn=355001&storeId=10161#reviews"

consoles = [ps5digital, ps5disc, ps5ratchet]

# send_keep_alive("I'm alive. Kotsovolos")


class KotsovolosConsolesSpider(scrapy.Spider):
    name = 'kotsovolos_consoles'
    allowed_domains = ['www.kotsovolos.cy']
    start_urls = consoles

    def parse(self, response):
        try:
            product_name = response.css('li.current::text').extract()
            time.sleep(5)
            availability = response.css('.PdpButtons > .button::text').extract()

            row_data = zip(product_name, availability)

            for item in row_data:
                scraped_info = {
                    'product_name': strip(item[0]),
                    # 'price_range': item[1],
                    'availability': strip(item[1]),
                }

                if scraped_info['availability'] != 'Εξαντλήθηκε' and scraped_info['availability'] != '':
                    send('me', "\n".join(scraped_info.values()) + '\n' + response.url)
                    send('chat', "\n".join(scraped_info.values()) + '\n' + response.url)
        except:
            send('me', 'I died. Kotsovolos')
