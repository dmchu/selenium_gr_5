import random
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


@pytest.fixture
def driver(request):
    driver = webdriver.Chrome()
    driver.implicitly_wait(2)
    request.addfinalizer(driver.quit)
    return driver


def test_external_links(driver):
    wait = WebDriverWait(driver, 5)
    driver.get("http://localhost/litecart/admin")

    driver.find_element_by_name("username").send_keys("admin")
    driver.find_element_by_name("password").send_keys("admin")
    driver.find_element_by_name("login").click()
    wait.until(EC.title_is("My Store"))

    menu = driver.find_element_by_id("box-apps-menu")
    menu.find_element(By.LINK_TEXT, "Countries").click()
    wait.until(EC.title_contains("Countries"))

    table = driver.find_element(By.CSS_SELECTOR, "table.dataTable")
    rows = table.find_elements(By.CSS_SELECTOR, ".row")

    countries = [row.find_element(By.TAG_NAME, 'a').text for row in rows]

    country = random.randrange(0,(len(countries)))

    driver.find_element(By.LINK_TEXT, countries[country]).click()

    external_links = driver.find_elements(By.CLASS_NAME, "fa-external-link")

    old_window = driver.current_window_handle
    new_window = None

    for external_link in external_links:
        external_link.click()
        wait.until(EC.new_window_is_opened)
        current_windows = driver.window_handles
        for window_id in current_windows:
            if window_id != old_window:
                new_window = window_id

        driver.switch_to_window(new_window)
        driver.close()
        driver.switch_to_window(old_window)