from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

class MainPage:

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def open(self):
        self.driver.get("http://localhost/litecart/en/")
        return self

    def select_products_to_buy(self,x):
        list_of_products = self.driver.find_elements(By.CSS_SELECTOR, ".content a.link")

        products = []
        for product in list_of_products:
            current_product = dict.fromkeys(['name', 'link'])
            current_product['name'] = product.find_element(By.CLASS_NAME, "name").get_attribute('textContent')
            current_product['link'] = product.get_attribute('href')
            products.append(current_product)
            if len(products) == x: break
        return products

    @property
    def products_in_cart(self):
        return self.driver.find_element(By.CSS_SELECTOR, '#cart .quantity').text