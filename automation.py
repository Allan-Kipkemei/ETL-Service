import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# ---- USER INPUT ----
USERNAME = "0710251692"
PASSWORD = "Amblessed9283F4y"
PHOTO_PATH = "./WIN_20250807_21_58_41_Pro.jpg"
CAPTION = "My automated post with Selenium 🚀"

# ---- SETUP BROWSER ----
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.get("https://www.instagram.com/accounts/login/")
driver.maximize_window()
time.sleep(5)

# ---- LOGIN ----
driver.find_element(By.NAME, "username").send_keys(USERNAME)
driver.find_element(By.NAME, "password").send_keys(PASSWORD + Keys.RETURN)
time.sleep(7)

# ---- CLOSE POPUPS (if shown) ----
try:
    driver.find_element(By.XPATH, "//button[contains(text(), 'Not Now')]").click()
    time.sleep(3)
except:
    pass

# ---- GO TO CREATE POST PAGE ----
driver.get("https://www.instagram.com/create/select/")
time.sleep(5)

# ---- UPLOAD PICTURE ----
upload_input = driver.find_element(By.XPATH, "//input[@type='file']")
upload_input.send_keys(PHOTO_PATH)
time.sleep(5)

# ---- NEXT ----
driver.find_element(By.XPATH, "//div[text()='Next']").click()
time.sleep(3)
driver.find_element(By.XPATH, "//div[text()='Next']").click()
time.sleep(3)

# ---- ADD CAPTION ----
caption_area = driver.find_element(By.TAG_NAME, "textarea")
caption_area.send_keys(CAPTION)
time.sleep(2)

# ---- SHARE ----
driver.find_element(By.XPATH, "//div[text()='Share']").click()

print("✅ One picture posted successfully!")
time.sleep(10)
driver.quit()
