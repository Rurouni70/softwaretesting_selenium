import time

import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


link = 'http://localhost/litecart/admin/?app=countries&doc=countries'
login = 'admin'
password = 'admin'

@pytest.fixture
def driver(request):
    wd = webdriver.Chrome()
    request.addfinalizer(wd.quit)
    return wd


def test_for_lesson(driver):
    wait = WebDriverWait(driver, 10)
    driver.implicitly_wait(10)
    driver.get(link)
    driver.find_element_by_name("username").send_keys(login)
    driver.find_element_by_name("password").send_keys(password)
    driver.find_element_by_name("login").click()
    time.sleep(2)
    # edit = WebDriverWait(driver, 30).until(
    #     EC.element_to_be_clickable((By.CSS_SELECTOR, "i.fa.fa-pencil")))
    # edit = wait.until(EC.visibility_of(driver.find_element_by_css_selector("i.fa.fa-pencil")))
    edit = driver.find_element_by_css_selector("i.fa.fa-pencil")
    edit.click()

    time.sleep(2)
    list_tab = driver.find_elements_by_css_selector("i.fa.fa-external-link")
    len_list = len(list_tab)  # 7
    count = 0
    main_window = driver.current_window_handle  # Cтраница откуда открывются страницы

    while count < len_list:
        list_tab[count].click()
        time.sleep(5)
        all_open_tab = driver.window_handles  # Cписок открытых вкладкок

        driver.switch_to_window(all_open_tab[-1])

        driver.close()
        time.sleep(3)
        driver.switch_to_window(main_window)
        count += 1

