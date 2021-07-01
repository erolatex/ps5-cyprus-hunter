from .base_page import BasePage
from .locators import LoginPageLocators


class LoginPage(BasePage):
    def should_be_login_page(self):
        self.should_be_login_url()

    def should_be_login_url(self):
        assert "login" in self.browser.current_url, "It isn't login url"

    def login(self, email, password):
        login_field = self.browser.find_element(*LoginPageLocators.LOGIN_EMAIL_FIELD)
        login_field.send_keys(email)

        pass_field = self.browser.find_element(*LoginPageLocators.LOGIN_EMAIL_FIELD)
        pass_field.send_keys(password)

        register_button = self.browser.find_element(*LoginPageLocators.LOGIN_BUTTON)
        register_button.click()
