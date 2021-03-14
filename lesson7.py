import time

import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


link = 'http://localhost/litecart/en/'


@pytest.fixture
def driver(request):
    wd = webdriver.Chrome()
    request.addfinalizer(wd.quit)
    return wd


def test_for_lesson(driver):
    driver.get(link)
    first_product = driver.find_element_by_css_selector("li.product.column.shadow.hover-light")
    first_product.click()
    # time.sleep(2) Почему тест перестаёт падать, когда появляется тут задержка?

    add_to_cart = WebDriverWait(driver, 30).until(
        EC.visibility_of_element_located((By.XPATH, "//button[@name = 'add_cart_product']")))
    add_to_cart.click()

    WebDriverWait(driver, 5).until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, 'a.content'), '1'))
    add_to_cart.click()
    time.sleep(5)

