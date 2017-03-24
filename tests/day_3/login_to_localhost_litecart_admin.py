import pytest
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@pytest.fixture
def driver(request):
    wd = webdriver.Chrome()
    # wd = webdriver.Chrome(desired_capabilities={"chromeOptions": {"args": ['--start-fullscreen']}})
    # wd = webdriver.Safari()
    # wd = webdriver.Firefox()
    # wd = webdriver.Firefox(firefox_binary="/Applications/FirefoxNightly.app/Contents/MacOS/firefox-bin")
    # wd = webdriver.Firefox(firefox_binary="/Applications/firefox_ESR45/Firefox.app/Contents/MacOS/firefox-bin", capabilities={"marionette": False})
    # wd = webdriver.Firefox(firefox_binary="/Applications/Firefox.app/Contents/MacOS/firefox-bin", capabilities={"marionette": True})
    # wd = webdriver.Firefox(capabilities={"marionette": False}) # старая схема Firefox ESR 45
    # wd.maximize_window()

    print(wd.capabilities)
    wd.implicitly_wait(10)
    request.addfinalizer(wd.quit)
    return wd

def test_example(driver):

    driver.get("http://localhost/litecart/admin/")

    driver.find_element_by_name("username").clear()
    driver.find_element_by_name("username").send_keys("admin")
    driver.find_element_by_name("password").send_keys("admin")
    driver.find_element_by_name("login").click()

    WebDriverWait(driver, 10).until(EC.title_is("My Store"))
