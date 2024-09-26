from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from time import sleep
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException, NoSuchElementException,ElementNotInteractableException
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException,StaleElementReferenceException

# Setup options for headless mode
opt = Options()
# opt.add_argument('--headless')

# Correct the path to chromedriver
serv_obj = Service(r"E:\browser-drivers\chromedriver.exe")

# Initialize the WebDriver with the correct argument
driver = webdriver.Chrome(service=serv_obj, options=opt)
driver.implicitly_wait(3)
U="a1bcz1a1342@gmail.com"

# Open Site 
driver.get("https://www.demoblaze.com")
driver.maximize_window()
# Signup
# Signup with valid details
driver.find_element(By.XPATH,"//a[@id='signin2']").click()
driver.find_element(By.XPATH,"//input[@id='sign-username']").send_keys(U)
driver.find_element(By.XPATH,"//input[@id='sign-password']").send_keys("1234")
driver.find_element(By.XPATH,"//button[normalize-space()='Sign up']").click()

try:
    WebDriverWait(driver, 10).until(EC.alert_is_present())
    alert = driver.switch_to.alert
    alert_text = alert.text

    if alert_text == "Sign up successful.":
        print("Signup with valid details test case passed")
    else:
        print(f"Unexpected alert message: {alert_text}")
    
    alert.accept()  # Close the alert

except TimeoutException:
    print("Signup alert did not appear. Test case failed")

sleep(5)

# Negative scenario Signup again with same valid details
driver.refresh()
driver.find_element(By.XPATH,"//a[@id='signin2']").click()
driver.find_element(By.XPATH,"//input[@id='sign-username']").send_keys(U)
driver.find_element(By.XPATH,"//input[@id='sign-password']").send_keys("1234")
driver.find_element(By.XPATH,"//button[normalize-space()='Sign up']").click()

try:
    WebDriverWait(driver, 10).until(EC.alert_is_present())
    alert = driver.switch_to.alert
    alert_text = alert.text

    if alert_text == "Sign up successful.":
        print("Signup with same details test case failed")
    else:
        print(f"Negative scenario passed alert message: {alert_text}")
    
    alert.accept()  # Close the alert

except TimeoutException:
    print("Signup alert did not appear. Test case failed")

sleep(5)

# Negative scenario: Attempt to log in with invalid credentials.
driver.refresh()
driver.find_element(By.XPATH,"//a[@id='login2']").click()
driver.find_element(By.XPATH,"//input[@id='loginusername']").send_keys("12345")
driver.find_element(By.XPATH,"//input[@id='loginpassword']").send_keys("1234")
driver.find_element(By.XPATH,"//button[normalize-space()='Log in']").click()
try:
    WebDriverWait(driver, 10).until(EC.alert_is_present())
    alert = driver.switch_to.alert
    alert_text = alert.text
    if alert_text == "Wrong password.":
        print("Negative scenario: Attempt to log in with invalid credentials test case passed")
    else:
        print(f"Negative scenario failed alert message: {alert_text}")    

    alert.accept()  # Close the alert

except TimeoutException:
    print("Negative scenario login alert did not appear. Test case failed")

# Positive scenario: Log in with valid credentials.
driver.refresh()
driver.find_element(By.XPATH,"//a[@id='login2']").click()
driver.find_element(By.XPATH,"//input[@id='loginusername']").send_keys(U)
driver.find_element(By.XPATH,"//input[@id='loginpassword']").send_keys("1234")
driver.find_element(By.XPATH,"//button[normalize-space()='Log in']").click()
# Check for successful login by looking for "nameofuser" element
try:
    user_element = driver.find_element(By.XPATH, "//a[@id='nameofuser']")
    print("Test case Log in with valid credentials passed")
except NoSuchElementException:
    print("Test case Log in with valid credentials failed")

# Verify that products are displayed correctly on the homepage.
a=driver.find_element(By.XPATH,"//a[normalize-space()='Samsung galaxy s6']").text
b=driver.find_element(By.XPATH,"//*[@id='article']").text
if a.lower() in b.lower():
    print("Products are displayed correctly test case passed")
else:
    print("products are not displayed correctly test case failed")
sleep(5)

try:
    driver.find_element(By.XPATH, "//a[@id='itemc' and @onclick=\"byCat('notebook')\"]").click()
    driver.find_element(By.XPATH, "//a[normalize-space()='Sony vaio i5']").click()
    driver.back()
    print("Product categories can be navigated successfully test case passed")
except Exception as e:
    # Verify that product categories can be navigated successfully.

    print(f"Product categories cannot be navigated successfully. Test case failed. Reason: {str(e)}")

# Navigate to the last page by clicking next

try:
    while True:
        print("Waiting for the Next button to become clickable...")
        
        try:
            # Wait until the Next button is clickable
            next_button = WebDriverWait(driver, 15).until(  # Increased timeout to 15 seconds
                EC.element_to_be_clickable((By.XPATH, "//button[@id='next2']"))
            )
        except TimeoutException:
            print("No more pages to navigate. Reached the last page.")
            break  # Exit the loop if the button is not found

        # Scroll into view if necessary
        driver.execute_script("arguments[0].scrollIntoView();", next_button)

        # Click on the Next button
        next_button.click()
        print("Clicked on the Next button.")
        sleep(2)  # Wait for the next page to load

except NoSuchElementException:
    print("No more pages to navigate. Reached the last page.")

except ElementClickInterceptedException:
    print("The next button could not be clicked due to another element overlaying it.")

except StaleElementReferenceException:
    print("The next button is no longer in the DOM. Exiting the loop.")

except ElementNotInteractableException:
    print("The next button is not interactable. Possible reasons include it being hidden or not yet rendered.")

except Exception as e:
    print(f"An unexpected error occurred: {e}")

# select the last product and add the product to the cart.
elements=driver.find_elements(By.XPATH,"//*[@class='col-lg-4 col-md-6 mb-4']")
lastelement=elements[-1]
lastelement.click()
sleep(2)
lastelementname=driver.find_element(By.XPATH,"//h2[@class='name']").text
driver.find_element(By.XPATH,"//a[normalize-space()='Add to cart']").click()
try:
    WebDriverWait(driver, 10).until(EC.alert_is_present())
    alert = driver.switch_to.alert
    alert_text = alert.text
    if alert_text == "Product added.":
        print("Add the last product to the cart test case passed")
    else:
        print(f"failed to add the last product to the cart alert message: {alert_text}")    

    alert.accept()  # Close the alert

except TimeoutException:
    print("add the product to the cart due to timeout Test case failed ")

# Positive scenario: Successfully check the items added to the cart.
driver.find_element(By.XPATH,"//a[normalize-space()='Cart']").click()
nameincart=driver.find_element(By.XPATH,"//table[@class='table table-bordered table-hover table-striped']/tbody/tr[1]/td[2]").text
if lastelementname==nameincart: 
    print("Correct product added")
else:
    print("Incorrect product added")

# Negative scenario: Attempt to checkout without adding any products to the cart.
driver.find_element(By.XPATH,"//a[normalize-space()='Delete']").click()
driver.find_element(By.XPATH,"//button[normalize-space()='Place Order']").click()
if driver.find_element(By.XPATH,"//h5[@id='orderModalLabel']"):
    print("I am able to place order on empty cart. Negative Test case failed")
else:
    print("Negative test case passed")

# Positive scenario: Successfully log out.
driver.refresh()
driver.find_element(By.XPATH,"//a[@id='logout2']").click()
print("Logged out successfully")

# Close the browser after test completion
driver.quit()
