import os
import sys
import scrapy
from lxml.doctestcompare import strip

sys.path.insert(0, os.path.abspath('..'))
from telegram import send, send_keep_alive

ps5digital = "https://sonycentercy.com/playstation-5/2187-sony-playstation-5-digital-edition-0711719395102.html"
ps5disc = "https://sonycentercy.com/playstation-5/2186-sony-playstation-5-0711719395003.html"

testProduct = "https://sonycentercy.com/in-ear/2516-sony-mdr-e9lp-headphones-orange-white.html"

consoles = [ps5digital, ps5disc]

# send_keep_alive("I'm alive. Sonycentercy")


class SonycentercyConsolesSpider(scrapy.Spider):
    name = 'sonycentercy_consoles'
    allowed_domains = ['sonycentercy.com']
    start_urls = consoles

    def parse(self, response):
        try:
            product_name = response.css('.h1[itemprop="name"]::text').extract()
            price_range = response.css('div.current-price > span[itemprop="price"]::text').extract()
            availability = response.css('button[class="btn btn-primary add-to-cart"]::text').extract()

            row_data = zip(product_name, price_range, availability)

            for item in row_data:
                scraped_info = {
                    'product_name': item[0],
                    'price_range': item[1],
                    'availability': strip(item[2]),
                }
                if scraped_info['availability'] != 'out of stock':
                    send('me', "\n".join(scraped_info.values()) + '\n' + response.url)
                    send('chat', "\n".join(scraped_info.values()) + '\n' + response.url)
        except:
            send('me', 'I died. Sonycentercy')
