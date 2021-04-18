import time

import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.select import Select

link = 'http://localhost/litecart/en/'


@pytest.fixture
def set_driver(request):
    wd = webdriver.Chrome()
    wd.implicitly_wait(0.5)
    request.addfinalizer(wd.quit)
    return wd


def test_for_lesson(set_driver):
    driver = set_driver
    driver.get(link)
    add_to_cart(driver, 3)
    cart = driver.find_element_by_xpath('//a[text()="Checkout »"]')
    cart.click()

    count_products_in_cart = driver.find_elements_by_xpath(
        '//td[@class="item"]')

    i = 1
    while i <= len(count_products_in_cart):
        product_name = driver.find_element_by_xpath('//li//strong').text
        table_product_name = driver.find_element_by_xpath(
            '//td[text() = "%s"]' % product_name)

        remove_button = driver.find_element_by_xpath(
            '//button[@name="remove_cart_item"]')
        remove_button.click()

        WebDriverWait(driver, 10).until(EC.staleness_of(table_product_name))
        i += 1


def add_to_cart(driver, items):
    i = 1
    while i <= items:

        products = driver.find_elements_by_xpath(
            "//li[contains(@class,'product column')]")
        products[0].click()

        try:
            select_size = Select(driver.find_element_by_xpath(
                '//select[@name="options[Size]"]'))
            select_size.select_by_value("Medium")
        except NoSuchElementException:
            pass

        button_add_to_cart = driver.find_element_by_xpath(
            '//button[@name="add_cart_product"]')
        button_add_to_cart.click()

        WebDriverWait(driver, 10).until(
            lambda d, x=i: d.find_element_by_xpath(
                '//span[@class="quantity" and text()=%s]' % x))

        logotype_link = driver.find_element_by_xpath(
            '//div[@id="logotype-wrapper"]/a')
        logotype_link.click()
        i += 1
