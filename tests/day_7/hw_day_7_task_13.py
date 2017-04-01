import pytest
from faker import Faker
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait
from wheel.signatures import assertTrue


@pytest.fixture
def driver(request):
    driver = webdriver.Chrome()
    driver.implicitly_wait(2)
    request.addfinalizer(driver.quit)
    return driver


def test_cart(driver):
    wait = WebDriverWait(driver, 5)
    f = Faker()
    driver.get("http://localhost/litecart/en/")

    number_of_products_to_buy = 3
    list_of_products = driver.find_elements(By.CSS_SELECTOR, ".content a.link")

    products = []
    for product in list_of_products:
        current_product = dict.fromkeys(['name', 'link'])
        current_product['name'] = product.find_element(By.CLASS_NAME, "name").get_attribute('textContent')
        current_product['link'] = product.get_attribute('href')
        products.append(current_product)
        if len(products) == number_of_products_to_buy: break

    added_to_cart_products =[]
    for product_page in products:
        driver.find_element(By.CSS_SELECTOR, 'a.link[href="{}"]'.format(product_page['link'])).click()
        # verify if the product has size
        size = driver.find_elements(By.NAME, "options[Size]")
        if len(size) == 1:
            Select(driver.find_element(By.NAME, "options[Size]")).select_by_visible_text("Small")
        cart_items_before = driver.find_element(By.CSS_SELECTOR, '#cart .quantity').text
        add_to_cart = driver.find_element(By.NAME, "add_cart_product")
        add_to_cart.click()
        cart_items_now = str(int(cart_items_before) + 1)
        wait.until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, '#cart .quantity'), cart_items_now))

        driver.find_element(By.CSS_SELECTOR, '*[title="Home"]').click()

    checkout = driver.find_element(By.LINK_TEXT, "Checkout »")
    checkout.click()

    products_shortcuts = len(driver.find_elements(By.CLASS_NAME, "shortcut"))
    driver.find_element(By.CLASS_NAME, "shortcut").click()

    while products_shortcuts > 0:

        product_info = driver.find_element(By.CSS_SELECTOR, ".item>form>div")
        product_info_text = product_info.find_element(By.TAG_NAME, "a").text
        product_in_table_summary = driver.find_element(By.CSS_SELECTOR, '#box-checkout-summary td.item')
        assertTrue(product_info_text == product_in_table_summary.text, "Product does not exist in table")
        driver.find_element(By.NAME, "remove_cart_item").click()
        wait.until(EC.staleness_of(product_in_table_summary))
        products_shortcuts -= 1

    driver.find_element(By.LINK_TEXT, "<< Back").click()
    cart_items_after = driver.find_element(By.CSS_SELECTOR, '#cart .quantity').text
    assertTrue(cart_items_after == "0", "Not all products removed from the cart")