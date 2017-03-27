import pytest
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from wheel.signatures import assertTrue


@pytest.fixture
def driver(request):
    wd = webdriver.Chrome()
    wd.implicitly_wait(2)
    request.addfinalizer(wd.quit)
    return wd


def test_countries_order(driver):
    wait = WebDriverWait(driver, 5)
    driver.get("http://localhost/litecart/admin")

    driver.find_element_by_name("username").send_keys("admin")
    driver.find_element_by_name("password").send_keys("admin")
    driver.find_element_by_name("login").click()
    wait.until(EC.title_is("My Store"))

    # 1) на странице http://localhost/litecart/admin/?app=countries&doc=countries

    driver.find_element_by_link_text('Countries').click()
    wait.until(EC.title_contains("Countries"))

    table = driver.find_element(By.CSS_SELECTOR, "table.dataTable")
    rows = table.find_elements(By.CSS_SELECTOR, ".row")

    # a) проверить, что страны расположены в алфавитном порядке

    row = driver.find_element(By.TAG_NAME, 'a')
    countries = [row.find_element(By.TAG_NAME, 'a').text for row in rows]
    assertTrue(countries == sorted(countries), "Countries are not in the alphabetical order")

    # b) для тех стран, у которых количество зон отлично от нуля -- открыть страницу этой страны
    #  и там проверить, что зоны расположены в алфавитном порядке

    countries_with_zones = [row.find_element(By.TAG_NAME, 'a').text for row in rows
                            if int(row.find_element(By.CSS_SELECTOR, "td:nth-child(6)").text) > 0]

    for country in countries_with_zones:
        driver.find_element(By.LINK_TEXT, country).click()

        sub_table = driver.find_element(By.ID, "table-zones")
        sub_rows = sub_table.find_elements(By.XPATH, ".//a[@id='remove-zone']/../..")
        zones = [sub_row.find_element(By.CSS_SELECTOR, "td:nth-child(3)>input[type=hidden]").get_attribute("value") for sub_row in sub_rows]
        assertTrue(zones == sorted(zones), "Zones are not in the alphabetical order")

        driver.find_element_by_link_text('Countries').click()

        #   2) на странице http://localhost/litecart/admin/?app=geo_zones&doc=geo_zones
        #   зайти в каждую из стран и проверить, что зоны расположены в алфавитном порядке

    driver.find_element_by_link_text('Geo Zones').click()
    wait.until(EC.title_contains("Geo Zones"))
    table_rows = driver.find_elements(By.XPATH, './/table//tr/td[5]/a/../..')
    geo_zones = [row.find_element(By.XPATH, './/td[3]/a').text for row in table_rows]
    for geo_zone in geo_zones:
        driver.find_element_by_link_text(geo_zone).click()
        zones_table = driver.find_element(By.ID, "table-zones")
        zones_rows = zones_table.find_elements(By.XPATH, ".//td[4]//a/../..")
        zones = [sub_row.find_element(By.XPATH, ".//td[3]//option[@selected='selected']").get_attribute("textContent") for sub_row in zones_rows]
        assertTrue(zones == sorted(zones), "Zones are not in the alphabetical order")
        driver.find_element_by_link_text('Geo Zones').click()
