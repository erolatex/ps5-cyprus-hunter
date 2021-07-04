import os
import sys
import scrapy

sys.path.insert(0, os.path.abspath('..'))
from telegram import send, send_keep_alive

xbox = "https://buyaway.net/product/xbox-series-x-1tb/"
ps5digital = "https://buyaway.net/product/ps5-console-digital-edition/"
ps5disc = "https://buyaway.net/product/ps5-console/"

testProduct = "https://buyaway.net/product/pop-184-rocks-freddie-mercury-king/"

consoles = [ps5digital, ps5disc, xbox]


class BuyawayConsolesSpider(scrapy.Spider):
    name = 'buyaway_consoles'
    allowed_domains = ['buyaway.net']
    start_urls = consoles

    def parse(self, response):
        send_keep_alive("I'm alive. Buyaway")
        try:
            product_name = response.css('.product_title::text').extract()
            price_range = response.css('.price .amount::text').extract()
            availability = response.css('span > p.stock::text').extract()

            row_data = zip(product_name, price_range, availability)

            for item in row_data:
                scraped_info = {
                    'product_name': item[0],
                    'price_range': item[1],
                    'availability': item[2],
                }
                if scraped_info['availability'] != 'Out of stock':
                    send('me', "\n".join(scraped_info.values()) + '\n' + response.url)
                    send('chat', "\n".join(scraped_info.values()) + '\n' + response.url)
        except:
            send('me', 'I\'m died. Buyaway')
