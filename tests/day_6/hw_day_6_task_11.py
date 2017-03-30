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
    wd = webdriver.Chrome()
    wd.implicitly_wait(2)
    request.addfinalizer(wd.quit)
    return wd


def test_countries_order(driver):
    f = Faker()
    wait = WebDriverWait(driver, 5)


    driver.get("http://localhost/litecart/en/")

    login_box = driver.find_element(By.ID, 'box-account-login')
    create_new_account = login_box.find_element(By.LINK_TEXT, "New customers click here")
    create_new_account.click()

    user_details = dict.fromkeys(
        ['First Name', 'Last Name', 'Address', 'Postcode', 'City', 'State',
         'Email', 'Phone', 'Password'])
    user_details['First Name'] = f.first_name()
    user_details['Last Name'] = f.last_name()
    user_details['Address'] = f.street_address()
    user_details['Postcode'] = f.postalcode()
    user_details['City'] = f.city()
    user_details['State'] = f.state()
    user_details['Email'] = f.email()
    user_details['Phone'] = f.phone_number()
    user_details['Password'] = f.password()

    create_account = driver.find_element(By.ID, 'create-account')


    create_account_form = dict.fromkeys(
        ['First Name', 'Last Name', 'Address', 'Postcode', 'City', 'State',
         'Email', 'Phone', 'Password'])
    create_account_form['First Name'] = create_account.find_element(By.NAME, 'firstname')
    create_account_form['Last Name'] = create_account.find_element(By.NAME, 'lastname')
    create_account_form['Address'] = create_account.find_element(By.NAME, 'address1')
    create_account_form['Postcode'] = create_account.find_element(By.NAME, 'postcode')
    create_account_form['City'] = create_account.find_element(By.NAME, 'city')
    create_account_form['State'] = create_account.find_element(By.CSS_SELECTOR, 'select[name="zone_code"]')
    create_account_form['Email'] = create_account.find_element(By.NAME, 'email')
    create_account_form['Phone'] = create_account.find_element(By.NAME, 'phone')
    create_account_form['Password'] = create_account.find_element(By.NAME, 'password')
    create_account_form['Confirm Password'] = create_account.find_element(By.NAME, 'confirmed_password')
    # Fill in the form

    create_account_form['First Name'].send_keys(user_details['First Name'])
    create_account_form['Last Name'].send_keys(user_details['Last Name'])
    create_account_form['Address'].send_keys(user_details['Address'])
    create_account_form['Postcode'].send_keys(user_details['Postcode'])
    create_account_form['City'].send_keys(user_details['City'])
    # Select Country
    country = 'United States'
    select_country = driver.find_element(By.CSS_SELECTOR, 'select')
    countries = select_country.text.split('\n  ')
    driver.execute_script("arguments[0].selectedIndex = {}; "
        "arguments[0].dispatchEvent(new Event('change'))".format(countries.index(country)), select_country)
    # Select State
    Select(create_account_form['State']).select_by_visible_text('{}'.format(user_details['State']))

    create_account_form['Email'].send_keys(user_details['Email'])
    create_account_form['Phone'].send_keys("111-333-444")
    create_account_form['Password'].send_keys(user_details['Password'])
    create_account_form['Confirm Password'].send_keys(user_details['Password'])

    create_account.find_element(By.NAME, 'create_account').click()

    success_create = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".notice.success")))
    assertTrue(success_create.text == "Your customer account has been created.", "account has not been created")


    account_box = driver.find_element(By.ID, "box-account")
    logout = account_box.find_element(By.LINK_TEXT, "Logout")
    logout.click()

    # Second login

    login_box = driver.find_element(By.ID, 'box-account-login')
    email_field = login_box.find_element(By.NAME, "email")
    password_field = login_box.find_element(By.NAME, "password")

    email_field.send_keys(user_details['Email'])
    password_field.send_keys(user_details['Password'])

    login = login_box.find_element(By.NAME, "login")
    login.click()

    success_login = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".notice.success")))
    assertTrue(success_login.text == "You are now logged in as {0} {1}.".format(user_details['First Name'],
               user_details['Last Name']), "User's full name doesn't much!")

    account_box = driver.find_element(By.ID, "box-account")
    logout = account_box.find_element(By.LINK_TEXT, "Logout")
    logout.click()