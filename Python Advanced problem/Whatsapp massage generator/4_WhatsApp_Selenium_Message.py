
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

contact = "Shreya Gupta Roommate Pg"
text = "Hey, this message was sent using Selenium"

# ✅ Use correct way to initialize ChromeDriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

driver.get("https://web.whatsapp.com")
print("Scan the QR code and press Enter when done...")
input("Press Enter after scanning QR code...")

print("Logged In")

# Search box for contacts
inp_xpath_search = "//div[@title='Search input textbox']"

# Wait for WhatsApp to load
WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.XPATH, inp_xpath_search)))
search_box = driver.find_element(By.XPATH, inp_xpath_search)
search_box.click()
search_box.send_keys(contact)
time.sleep(2)

# Select contact from list
selected_contact = WebDriverWait(driver, 30).until(
    EC.presence_of_element_located((By.XPATH, f"//span[@title='{contact}']"))
)
selected_contact.click()

# Find the message input box
msg_box_xpath = "//div[@title='Type a message']"
input_box = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, msg_box_xpath)))
input_box.send_keys(text + Keys.ENTER)

print("✅ Message sent!")

time.sleep(2)
driver.quit()
