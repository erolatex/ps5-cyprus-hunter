from .base_page import BasePage
from .locators import ProductPageLocators

import telegram as tg


class ProductPage(BasePage):

    def is_product_available(self):
        if self.is_element_present(*ProductPageLocators.OUT_OF_STOCK):
            return False
        return True

    def check_product_availability(self):
        if self.is_product_available():
            tg.send('me', self.grab_name() + "\n" + self.browser.current_url + "\n" + self.grab_prices())
            tg.send('chat', self.grab_name() + "\n" + self.browser.current_url + "\n" + self.grab_prices())

    def grab_prices(self):
        return self.browser.find_element(*ProductPageLocators.PRODUCT_PRICE).text

    def grab_name(self):
        return self.browser.find_element(*ProductPageLocators.PRODUCT_NAME).text
