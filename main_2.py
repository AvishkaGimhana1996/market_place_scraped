from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import time
import pandas as pd
import os
import csv
from datetime import datetime

# Set up the Chrome driver
chrome_driver_path = "Drivers/chromedriver.exe"  # Path to your chromedriver executable
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--disable-notifications")
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
time.sleep(5)  # Adjust as needed

# Open the Facebook Marketplace page
marketplace_url = 'https://www.facebook.com/marketplace/category/propertyforsale'
driver.get(marketplace_url)

for i in range(0):  # Adjust the range as needed
    driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.PAGE_DOWN)
    time.sleep(2)  # Wait for page to load

# Collect links of the posts
post_links = []
posts = driver.find_elements(By.CSS_SELECTOR, 'a[href^="/marketplace/item/"]')
for post in posts:
    post_links.append(post.get_attribute('href'))

# Collect heading and location of each post
post_data = []
for link in post_links:
    driver.get(link)
    time.sleep(2)  # Wait for the post page to load

    try:
        heading_element = driver.find_element(By.XPATH,'/html/body/div[1]/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div[2]/div/div/div/div/div/div[1]/div[2]/div/div[2]/div/div[1]/div[1]/div[1]/h1/span')
        heading = heading_element.text
    except NoSuchElementException:
        heading = "Heading not found"

    try:
        location_element = driver.find_element(By.XPATH,'/html/body/div[1]/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div[2]/div/div/div/div/div/div[1]/div[2]/div/div[2]/div/div[1]/div[1]/div[7]/div[3]/div/div[1]/span')
        location = location_element.text
    except NoSuchElementException:
        location = "Location not found"

    try:
        price_element=driver.find_element(By.XPATH,'/html/body/div[1]/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div[2]/div/div/div/div/div/div[1]/div[2]/div/div[2]/div/div[1]/div[1]/div[1]/div[1]/div/span')
        price=price_element.text
    except NoSuchElementException:
        price="Price not found"

    # Click "See More" button if it exists
    try:
        see_more_button = driver.find_element(By.XPATH, "/html/body/div[1]/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div[2]/div/div/div/div/div/div[1]/div[2]/div/div[2]/div/div[1]/div[1]/div[8]/div[2]/div/div/div/span/div")
        see_more_button.click()
        time.sleep(1)  # Wait for the content to load
    except NoSuchElementException:
        pass  # If the button is not found, do nothing

    try:
        description_element=driver.find_element(By.XPATH,'/html/body/div[1]/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div[2]/div/div/div/div/div/div[1]/div[2]/div/div[2]/div/div[1]/div[1]/div[8]/div[2]/div/div/div/span')
        description=description_element.text
    except NoSuchElementException:
        description="Description not found"

    try:
        link_element = driver.find_element(By.CSS_SELECTOR, 'a[href^="/marketplace/profile/"]')
        link_element.click()    
        time.sleep(2)
    except NoSuchElementException as e:
        pass

    try:
        profile_link_elements=driver.find_element(By.CSS_SELECTOR,'a[aria-label="View Profile"]')
        profile_link=profile_link_elements.get_attribute('href')
    
    except NoSuchElementException as e:
        profile_link='Profile link not found'
    

    try:
        profile_name_element=driver.find_element(By.XPATH,'/html/body/div[1]/div/div[1]/div/div[5]/div/div/div[2]/div/div/div/div/div/div/div/div[2]/div[2]/div/div[1]/div/div[1]/div/div[2]/div/div/div[2]/div/div/div[1]')
        profile_name=profile_name_element.text
    except:
        profile_name='profile name not found'
    
    post_data.append({'link': link, 'heading': heading, 'location': location,'price':price,'description':description,'profile_link':profile_link,'profile_name':profile_name})

# Close the driver
driver.quit()
# print(post_data)

current_date=datetime.now().strftime('%Y-%m-%d %H:%M:%S')

for data in post_data:
    data['upload_date'] = current_date



# Write the data to a CSV file
with open(os.path.join(os.getcwd(),'src', 'post_data.csv'), mode='w', newline='', encoding='utf-8') as file:
    fieldnames = ['link', 'heading', 'location','price','description','profile_link','profile_name','upload_date']
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()
    for data in post_data:
        writer.writerow(data)

print("Data written to CSV file successfully.")


