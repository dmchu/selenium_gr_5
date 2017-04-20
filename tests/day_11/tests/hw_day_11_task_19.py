import pytest
from selenium import webdriver
from wheel.signatures import assertTrue

from tests.day_11.pages.cart_page import CartPage
from tests.day_11.pages.main_page import MainPage
from tests.day_11.pages.product_page import ProductPage


@pytest.fixture
def driver(request):
    driver = webdriver.Chrome()
    driver.implicitly_wait(2)
    request.addfinalizer(driver.quit)
    return driver


def test_cart(driver):
    main_page = MainPage(driver)
    product_page = ProductPage(driver)
    cart_page = CartPage(driver)


    main_page.open()

    selected_products = main_page.select_products_to_buy(3)

    product_page.add_to_cart(selected_products)

    cart_page.remove_all_products_from_cart()

    cart_items = main_page.products_in_cart

    assertTrue(cart_items == "0", "Not all products removed from the cart")