import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@pytest.fixture
def browser():
    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)
    yield driver
    driver.quit()

def test_add_to_cart(browser):
    browser.get("http://localhost:5000")

    try:
        WebDriverWait(browser, 10).until(EC.title_contains("5 Fruits and Veggies"))
    except:
        print("Page did not load within the specified time")
    
    assert "5 Fruits and Veggies" in browser.title
