import pytest
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@pytest.fixture
def driver(request):
    wd = webdriver.Chrome()
    wd.implicitly_wait(10)
    request.addfinalizer(wd.quit)
    return wd


def test_example(driver):

    driver.get("http://google.com/")

    element_q=driver.find_element_by_name("q")
    # driver.refresh()
    driver.find_element_by_id("gs_ok0").click()
    driver.find_element_by_id("K32").click()
    driver.find_element_by_id("gs_ok0").click()


    element_q.send_keys("webdriver")
    driver.find_element_by_name("btnG").click()
    WebDriverWait(driver, 10).until(EC.title_is("webdriver - Поиск в Google"))

