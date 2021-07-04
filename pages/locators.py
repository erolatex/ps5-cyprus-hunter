from selenium.webdriver.common.by import By


class BasePageLocators(object):
    LOGIN_LINK = (By.CSS_SELECTOR, ".account-drop")
    CART_LINK = (By.CSS_SELECTOR, ".btn-group > a")
    USER_ICON = (By.CSS_SELECTOR, ".icon-user")


class MainPageLocators(object):
    LOGIN_LINK = (By.CSS_SELECTOR, "#login_link")
    LOGIN_LINK_INVALID = (By.CSS_SELECTOR, "#login_link")


class LoginPageLocators(object):
    LOGIN_FORM = (By.CSS_SELECTOR, "#login_form")
    REGISTER_FORM = (By.CSS_SELECTOR, "#register_form")
    LOGIN_BUTTON = (By.CSS_SELECTOR, "button[type=submit]")
    LOGIN_EMAIL_FIELD = (By.CSS_SELECTOR, "[name='spree_user[email]']")
    LOGIN_PASSWORD_FIELD = (By.CSS_SELECTOR, "[name='spree_user[password]']")


class ProductPageLocators(object):
    BUTTON_ADD_TO_BACKET = (By.CSS_SELECTOR, ".btn-add-to-basket")
    MESSAGE_ABOUT_ADDING = (By.CSS_SELECTOR, "div.alertinner ")
    PRODUCT_NAME = (By.CLASS_NAME, "product-title")
    MESSAGE_BASKET_TOTAL = (By.CSS_SELECTOR, ".alert-info .alertinner strong")
    PRODUCT_PRICE = (By.CSS_SELECTOR, ".product-prices-wrapper")
    OUT_OF_STOCK = (By.CSS_SELECTOR, ".icon-out-of-stock.stock-message > span")


class CartPageLocators(object):
    MESSAGE_EMPTY = (By.CSS_SELECTOR, "#content_inner > p")
    ITEMS = (By.CSS_SELECTOR, ".basket-items")

    MESSAGE_BASKET_TOTAL = (By.CSS_SELECTOR, ".alert-info .alertinner strong")
    PRODUCT_PRICE = (By.CSS_SELECTOR, ".product_main .price_color")
