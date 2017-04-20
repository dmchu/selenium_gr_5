from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait


class ProductPage:

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def add_to_cart(self, selected_products):
        for product_page in selected_products:
            self.driver.find_element(By.CSS_SELECTOR, 'a.link[href="{}"]'.format(product_page['link'])).click()
            size = self.driver.find_elements(By.NAME, "options[Size]")
            if len(size) == 1:
                Select(self.driver.find_element(By.NAME, "options[Size]")).select_by_visible_text("Small")
            cart_items_before = self.driver.find_element(By.CSS_SELECTOR, '#cart .quantity').text
            add_to_cart = self.driver.find_element(By.NAME, "add_cart_product")
            add_to_cart.click()
            cart_items_now = str(int(cart_items_before) + 1)
            self.wait.until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, '#cart .quantity'), cart_items_now))

            self.driver.find_element(By.CSS_SELECTOR, '*[title="Home"]').click()