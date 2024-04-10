

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import time
import urllib.parse
from message_sent import message_data
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC




# Set up the Chrome driver
chrome_driver_path = "Drivers/chromedriver.exe"  # Path to your chromedriver executable
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--disable-notifications")
chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                     "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36")
service = Service(chrome_driver_path)

driver = webdriver.Chrome(service=service, options=chrome_options)
url = 'https://www.facebook.com'
driver.get(url)

# Log in to Facebook
email = 'put_email_or_phone_number'
password = 'password'
email_element = driver.find_element(By.ID, 'email')
password_element = driver.find_element(By.ID, 'pass')
login_button = driver.find_element(By.NAME, 'login')

email_element.send_keys(email)
password_element.send_keys(password)
login_button.click()

# Wait for the login to complete
time.sleep(10)  # Adjust as needed

for profile_data in message_data:
    profile_link, message = profile_data[:2]  # Assuming profile_link is the first element and message is the second element in each sublist
    # print(message)
    

    try:
        driver.get(profile_link)
        time.sleep(5)

        try:
            message_element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "div[aria-label='Message']")))
            message_element.click()
            # print(message)
            time.sleep(5)

        except NoSuchElementException:
            pass

        try:
            chat_input = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div/div[1]/div/div[5]/div[1]/div[1]/div[1]/div/div/div/div/div/div/div/div[2]/div[2]/div/div/div/div[4]/div[2]/div/div[1]/div[1]/p")))
            chat_input.click()
            chat_input.send_keys(message)
            chat_input.send_keys(Keys.ENTER)
            # print(message)
            time.sleep(5)
        except NoSuchElementException:
            pass

        try:
            close_element=WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH,'/html/body/div[1]/div/div[1]/div/div[5]/div[1]/div[1]/div[1]/div/div/div/div/div/div/div/div[1]/div/div[2]/span[4]')))
            close_element.click()
            print(message)
            time.sleep(5)
        except:
            pass

    except Exception as e:
        print(f"Error navigating to URL: {profile_link}")
        print(e)
        continue

driver.quit()






