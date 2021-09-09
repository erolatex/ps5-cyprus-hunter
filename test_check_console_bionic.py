import os
import time

import pytest

from telegram import send_keep_alive
from telegram import send
from pages.product_page import ProductPage
from pages.login_page import LoginPage

xbox = "https://bionic.com.cy/products/xbox-series-x-1tb-ssd-with-1-controller"
ps5digital = "https://bionic.com.cy/products/sony-playstation-5-ps5-digital-edition-18300387"
ps5disc = "https://bionic.com.cy/products/sony-playstation-5-ps5-standard-edition"
ps5ratchet = "https://bionic.com.cy/products/sony-playstation-5-ps5-standard-edition-825gb-ssd-with-sft-game-ratchet" \
             "-clank-rift-apart "

testProduct = "https://bionic.com.cy/products/bny-power-bank-2800mah"
testProduct2 = "https://bionic.com.cy/products/xiaomi-mi-11-5g"

consoles = [ps5digital, ps5disc, ps5ratchet, xbox]
login = "https://bionic.com.cy/login"


class TestCheckConsoleBionic(object):
    @pytest.fixture(scope="function", autouse=True)
    def setup(self, browser):
        email = os.environ.get("BIONIC_LOGIN")
        password = os.environ.get("BIONIC_PASSWORD")
        login_page = LoginPage(browser, login)
        login_page.open()
        login_page.go_to_login_page()
        login_page.login(email, password)

    def test_consoles_bionic(self, browser):
        try:
            send_keep_alive('I\'m alive. Bionic')
            for product in consoles:
                page = ProductPage(browser, product)
                page.open()
                page.check_product_availability()
        except:
            send('me', 'I died. Bionic')
