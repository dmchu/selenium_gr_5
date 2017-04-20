from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from wheel.signatures import assertTrue


class CartPage:

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)


    def remove_all_products_from_cart(self):
        checkout = self.driver.find_element(By.LINK_TEXT, "Checkout »")
        checkout.click()

        products_shortcuts = len(self.driver.find_elements(By.CLASS_NAME, "shortcut"))
        self.driver.find_element(By.CLASS_NAME, "shortcut").click()

        while products_shortcuts > 0:
            product_info = self.driver.find_element(By.CSS_SELECTOR, ".item>form>div")
            product_info_text = product_info.find_element(By.TAG_NAME, "a").text
            product_in_table_summary = self.driver.find_element(By.CSS_SELECTOR, '#box-checkout-summary td.item')
            assertTrue(product_info_text == product_in_table_summary.text, "Product does not exist in table")
            self.driver.find_element(By.NAME, "remove_cart_item").click()
            self.wait.until(EC.staleness_of(product_in_table_summary))
            products_shortcuts -= 1

        self.driver.find_element(By.LINK_TEXT, "<< Back").click()