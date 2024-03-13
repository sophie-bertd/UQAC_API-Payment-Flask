import os

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from flask import url_for
import pytest

from orders_products.models import get_db

@pytest.mark.skipif('BROWSER_TEST' not in os.environ, reason="Browser tests will only run with --driver specified")
@pytest.mark.usefixtures('live_server')
class TestBrowser(object):
    def test_add_to_cart_js(self, selenium, app):
        wait = WebDriverWait(selenium, 10)

        response = selenium.get(url_for('index', _external=True))
        el_add_to_cart = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'addToCart')))
        el_add_to_cart.click()

        el_cart_item = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#cartSidebar .list-group-item')))
        assert "Product Name" in el_cart_item.text

    def test_cart_total_update_js(self, selenium, app):
        wait = WebDriverWait(selenium, 10)

        response = selenium.get(url_for('index', _external=True))
        el_add_to_cart = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'addToCart')))
        el_add_to_cart.click()

        el_cart_total = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '.cart-total')))
        assert "$" in el_cart_total.text

    def test_cart_sidebar_toggle_js(self, selenium, app):
        wait = WebDriverWait(selenium, 10)

        response = selenium.get(url_for('index', _external=True))
        el_cart_toggle = wait.until(EC.element_to_be_clickable((By.ID, 'cartToggle')))
        el_cart_toggle.click()

        el_cart_sidebar = wait.until(EC.visibility_of_element_located((By.ID, 'cartSidebar')))
        assert "open" in el_cart_sidebar.get_attribute("class")
