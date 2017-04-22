import pytest
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.events import EventFiringWebDriver, AbstractEventListener
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

class MyListener(AbstractEventListener):
    def before_find(self, by, value, driver):
        print(by, value)
    def after_find(self, by, value, driver):
        print(by, value, "found")
    def on_exception(self, exception, driver):
        print(exception)
@pytest.fixture
def driver(request):
    d = DesiredCapabilities.CHROME
    d['loggingPrefs'] = {'browser': 'ALL'}
    wd = EventFiringWebDriver(webdriver.Chrome(desired_capabilities=d), MyListener())
    wd.implicitly_wait(10)
    request.addfinalizer(wd.quit)
    return wd


def test_example(driver):

    driver.get("http://google.com/")
    for entry in driver.get_log('browser'):
        print(entry)

    element_q=driver.find_element_by_name("q")
    # driver.refresh()
    driver.find_element_by_id("gs_ok0").click()
    driver.find_element_by_id("K32").click()
    driver.find_element_by_id("gs_ok0").click()

    element_q.send_keys("webdriver")
    driver.find_element_by_name("btnG").click()
    WebDriverWait(driver, 10).until(EC.title_is("webdriver - Поиск в Google"))
    # driver.save_screenshot("switch_to_window_{}.jpg".format(random.randrange(1, 100)))
