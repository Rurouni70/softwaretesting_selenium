import pytest

from selenium import webdriver

from selenium.webdriver.support.wait import WebDriverWait


@pytest.fixture()
def set_driver(request):
    driver = webdriver.Chrome()
    driver.implicitly_wait(5)
    request.addfinalizer(driver.quit)
    return driver

def test_login(set_driver):
    driver = set_driver
    url = "http://localhost/litecart/admin/?app=countries&doc=countries"
    driver.get(url)
    driver.find_element_by_xpath('//input[@name="username"]').send_keys("admin")
    driver.find_element_by_xpath('//input[@name="password"]').send_keys("admin")
    driver.find_element_by_xpath('//button[@name="login"]').click()
    assert driver.find_element_by_xpath('//div[@class="logotype"]').is_enabled()

@pytest.mark.test10
def test_window(set_driver):
    driver = set_driver
    test_login(driver)

    countries = driver.find_element_by_xpath('//span[text()="Countries"]')
    countries.click()

    add_new_country = driver.find_element_by_xpath(
        '//div/a[contains (@href, "edit_country")]')

    add_new_country.click()

    external_links = driver.find_elements_by_xpath(
        '//i[@class="fa fa-external-link"]')

    main_window = driver.current_window_handle
    new_window_wait = WebDriverWait(driver, 10)

    for link in external_links:
        exciting_windows = driver.window_handles
        link.click()
        new_window = new_window_wait.until(NewWindowIsExists(exciting_windows))

        driver.switch_to.window(new_window)
        driver.close()
        driver.switch_to.window(main_window)

class NewWindowIsExists:
    def __init__(self, old_windows):
        self.old_windows = old_windows

    def __call__(self, driver):
        new_windows = driver.window_handles

        existing_windows = set(self.old_windows)
        new_windows = set(new_windows)

        diff = new_windows.difference(existing_windows)
        if len(diff) == 1:
            return diff.pop()

        return False