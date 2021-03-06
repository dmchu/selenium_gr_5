import pytest
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@pytest.fixture
def driver(request):
    # wd = webdriver.Chrome()
    wd = webdriver.Chrome(desired_capabilities={"chromeOptions": {"args": ['--start-fullscreen']}})
    #wd = webdriver.Safari()
    wd.maximize_window()
    # wd = webdriver.Firefox()
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
