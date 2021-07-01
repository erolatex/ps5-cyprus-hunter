from .base_page import BasePage
from .locators import CartPageLocators


class CartPage(BasePage):
    def should_be_cart_page(self):
        self.should_be_cart_link()

    def should_be_cart_link(self):
        # реализуйте проверку на корректный url адрес
        assert "basket" in self.browser.current_url, "It isn't cart url"

    def should_be_empty_cart(self):
        assert self.is_not_element_present(*CartPageLocators.ITEMS), \
            "Backet isn't empty"

    def should_be_message_empty(self):
        assert self.is_element_present(*CartPageLocators.MESSAGE_EMPTY), \
            "Message of empty isn't presented"

        message = self.browser.find_element(*CartPageLocators.MESSAGE_EMPTY).text
        assert message == "Your basket is empty. Continue shopping", \
            "Message about empty basket incorrect"
