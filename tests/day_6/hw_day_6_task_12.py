import os
from faker import Faker
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from wheel.signatures import assertTrue


@pytest.fixture
def driver(request):
    wd = webdriver.Chrome()
    wd.implicitly_wait(2)
    request.addfinalizer(wd.quit)
    return wd


def test_add_new_product(driver):
    wait = WebDriverWait(driver, 5)
    f = Faker()
    driver.get("http://localhost/litecart/admin")

    driver.find_element_by_name("username").send_keys("admin")
    driver.find_element_by_name("password").send_keys("admin")
    driver.find_element_by_name("login").click()

    wait.until(EC.title_is("My Store"))

    menu = driver.find_element_by_id("box-apps-menu")
    menu.find_element(By.LINK_TEXT, "Catalog").click()

    add_new_product = driver.find_element(By.LINK_TEXT, "Add New Product")
    add_new_product.click()

    tab_general = driver.find_element(By.ID, "tab-general")
    status_enabled = tab_general.find_element(By.CSS_SELECTOR, "input[value='1']")
    status_enabled.click()
    product_name = "Dark Blue Duck"
    product_name_field = tab_general.find_element(By.CSS_SELECTOR, ".input-wrapper>input")
    product_name_field.send_keys(product_name)
    code_field = tab_general.find_element(By.NAME, 'code')
    code_field.send_keys("rd006")
    categories = tab_general.find_elements(By.NAME, "categories[]")
    check = "Rubber Ducks"
    for category in categories:
        if category.get_attribute('checked') == "true":
            category.click()
        if category.get_attribute('data-name') == check:
            category.click()

    product_quantity = tab_general.find_element(By.NAME, "quantity")
    product_quantity.clear()
    product_quantity.send_keys(30)

    upload_image_field = tab_general.find_element(By.NAME, "new_images[]")
    path = os.path.normcase('tests/day_6/images/dark_blue_duck.png')
    absolute_path = os.path.abspath(path)

    upload_image_field.send_keys(absolute_path)

    # Information tab

    information_tab = driver.find_element(By.LINK_TEXT, "Information")
    information_tab.click()
    active_tab = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'active')))
    assertTrue(active_tab.text == "Information")

    info_form = driver.find_element(By.TAG_NAME, "table")

    manufacturer_select = info_form.find_element(By.NAME, "manufacturer_id")
    manufacturer = "ACME Corp."
    Select(manufacturer_select).select_by_visible_text(manufacturer)

    short_description = info_form.find_element(By.NAME, "short_description[en]")
    short_description_text = f.text(126)
    short_description.send_keys(short_description_text)

    description = info_form.find_element(By.CLASS_NAME, "trumbowyg-editor")
    description_text = f.text(669)
    description.send_keys(description_text)

    prices_tab = driver.find_element(By.LINK_TEXT, "Prices")
    prices_tab.click()
    active_tab = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'active')))
    assertTrue(active_tab.text == "Prices")

    prices_form = driver.find_element(By.TAG_NAME, "table")
    purchase_price = prices_form.find_element(By.NAME, "purchase_price")
    purchase_price.clear()
    purchase_price.send_keys(10)

    price = prices_form.find_element(By.NAME, "prices[USD]")
    price.clear()
    price.send_keys(20)

    save = driver.find_element(By.NAME, "save")
    save.click()

    success_message = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".notice.success")))
    assertTrue(success_message.text == "Changes were successfully saved.")

    assertTrue(driver.find_element(By.LINK_TEXT, product_name), "Product not exist")

