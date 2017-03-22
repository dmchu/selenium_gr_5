import pytest
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from wheel.signatures import assertTrue


@pytest.fixture
def driver(request):
    # wd = webdriver.Firefox()
    wd = webdriver.Chrome()
    # wd = webdriver.Chrome(desired_capabilities={"chromeOptions": {"args": ['--start-fullscreen']}})
    wd.implicitly_wait(2)
    request.addfinalizer(wd.quit)
    return wd

def test_left_menu(driver):

    driver.get("http://localhost/litecart/admin")

    driver.find_element_by_name("username").send_keys("admin")
    driver.find_element_by_name("password").send_keys("admin")
    driver.find_element_by_name("login").click()

    WebDriverWait(driver, 5).until(EC.title_is("My Store"))

    menu = driver.find_element_by_id("box-apps-menu")
    menu_items = []
    for menu_name in menu.find_elements_by_css_selector('.name'):
        menu_items.append(menu_name.text)
    for menu_item in menu_items:
        driver.find_element_by_link_text(menu_item).click()
        assertTrue(driver.find_element_by_tag_name('h1').is_displayed())

        sub_menu_items = []
        for sub_menu_name in driver.find_elements_by_css_selector('.docs .name'):
            sub_menu_items.append(sub_menu_name.text)
        for sub_menu_item in sub_menu_items:
            driver.find_element_by_link_text(sub_menu_item).click()
            assertTrue(driver.find_element_by_tag_name('h1').is_displayed())
