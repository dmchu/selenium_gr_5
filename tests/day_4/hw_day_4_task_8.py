import pytest
from selenium import webdriver
from wheel.signatures import assertTrue


@pytest.fixture
def driver(request):
    wd = webdriver.Firefox()
    # wd = webdriver.Chrome()
    wd.implicitly_wait(2)
    request.addfinalizer(wd.quit)
    return wd

def test_stikers(driver):
    driver.get("http://localhost/litecart")
    goods = driver.find_elements_by_class_name('name')
    for good in goods:
        sticker_numbers = len(good.find_elements_by_xpath(".//../div/div"))
        assertTrue(sticker_numbers == 1, "Number of stickers is not one!")
        assertTrue(good.find_element_by_xpath(".//../div/div").is_displayed(),"Sticker is not displayed!")

