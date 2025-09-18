import os
import time
import random
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# use undetected-chromedriver
import undetected_chromedriver as uc

# ---- USER INPUT ----
USERNAME = "0710251692"
PASSWORD = "Amblessed9283F4y"
# Prefer an absolute path
PHOTO_PATH = os.path.abspath("./WIN_20250807_21_58_41_Pro.jpg")
CAPTION = "My automated post with Selenium 🚀"

# small helper to randomize tiny delays (more human-like)
def tiny_sleep(a=0.6, b=1.4):
    time.sleep(random.uniform(a, b))

def main():
    options = uc.ChromeOptions()
    # Optional: run headless=False so you can see the browser
    options.add_argument("--start-maximized")
    # hide automation flags
    options.add_argument("--disable-blink-features=AutomationControlled")
    # set a common user agent (change if desired)
    options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.5790.98 Safari/537.36"
    )

    driver = uc.Chrome(options=options)

    wait = WebDriverWait(driver, 20)

    try:
        # ---- OPEN LOGIN PAGE ----
        driver.get("https://www.instagram.com/accounts/login/")
        # Wait for username field to appear
        username_el = wait.until(EC.presence_of_element_located((By.NAME, "username")))
        tiny_sleep()

        # ---- ENTER CREDENTIALS ----
        username_el.clear()
        username_el.send_keys(USERNAME)
        tiny_sleep(0.2, 0.6)

        pw_el = driver.find_element(By.NAME, "password")
        pw_el.clear()
        pw_el.send_keys(PASSWORD)
        tiny_sleep(0.3, 0.7)
        pw_el.send_keys(Keys.RETURN)

        # ---- WAIT FOR EITHER SUCCESS OR 2FA/ERROR ----
        # Wait until either the main page loads (presence of top-left Home icon) or we detect verification prompt
        # We'll wait for either:
        #  - presence of the "Create" (plus) element OR
        #  - presence of an element that indicates two-factor or checkpoint
        try:
            # Wait for typical logged-in element - the "New post" (plus) button can be inside header - we try a path that's likely stable
            wait.until(
                EC.presence_of_element_located(
                    (By.XPATH, "//div[@role='navigation'] | //header")
                )
            )
        except Exception:
            # not logged in cleanly - check for 2FA or challenge
            pass

        tiny_sleep()

        # ---- CHECK FOR 2FA / VERIFICATION FORMS ----
        page_source = driver.page_source.lower()
        if "two-factor" in page_source or "help us confirm" in page_source or "security code" in page_source or "enter code" in page_source:
            print("⚠️ Instagram is requesting 2FA / verification. Manual action required. Exiting.")
            driver.quit()
            return

        # Also check for checkpoint/challenge
        # For safety, detect if we are still on login page with errors
        if "login" in driver.current_url and ("challenge" in driver.current_url or "checkpoint" in driver.current_url):
            print("⚠️ Login challenge detected. Please complete verification in the browser. Exiting.")
            driver.quit()
            return

        # ---- DISMISS SAVE INFO / NOT NOW POPUPS IF THEY APPEAR ----
        tiny_sleep()
        try:
            # "Save Your Login Info?" -> Not Now
            not_now_btn = wait.until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//button[contains(., 'Not Now') or contains(., 'Not now')]")
                )
            )
            not_now_btn.click()
            tiny_sleep()
        except Exception:
            pass

        try:
            # "Turn on Notifications" -> Not Now
            not_now_btn2 = wait.until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//button[contains(., 'Not Now') or contains(., 'Not now') or contains(., 'Not now')]")
                ), timeout=5
            )
            not_now_btn2.click()
            tiny_sleep()
        except Exception:
            pass

        # ---- NAVIGATE TO CREATE POST ----
        # Instagram sometimes exposes a direct create URL
        driver.get("https://www.instagram.com/create/select/")
        # Wait until file input is present
        upload_input = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@type='file']")))

        tiny_sleep()

        # ---- VERIFY PHOTO PATH EXISTS ----
        if not os.path.exists(PHOTO_PATH):
            print(f"❌ Photo not found at {PHOTO_PATH}")
            driver.quit()
            return

        # ---- UPLOAD FILE ----
        upload_input.send_keys(PHOTO_PATH)
        # Wait until Next button is clickable (the text "Next" may be inside a button or div)
        # Instagram often uses aria-labels or role buttons; we'll search for clickable element with "Next"
        next_btn = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//button[.//div[text()='Next']] | //div[text()='Next' or .='Next'] | //button[contains(., 'Next')]")
            )
        )
        tiny_sleep()
        next_btn.click()
        tiny_sleep(1, 2)

        # Second Next (caption screen)
        # Wait and click the next again if present
        try:
            next_btn2 = wait.until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//button[.//div[text()='Next']] | //div[text()='Next' or .='Next'] | //button[contains(., 'Next')]")
                ), timeout=10
            )
            tiny_sleep()
            next_btn2.click()
        except Exception:
            # Sometimes one click is enough
            pass

        tiny_sleep(1, 2)

        # ---- ADD CAPTION ----
        # Caption area is usually a textarea with placeholder "Write a caption..."
        try:
            caption_area = wait.until(EC.presence_of_element_located((By.TAG_NAME, "textarea")))
            caption_area.click()
            tiny_sleep(0.5, 1.0)
            caption_area.send_keys(CAPTION)
        except Exception:
            # fallback: try an input with aria-label or contenteditable
            try:
                caption_area2 = driver.find_element(By.CSS_SELECTOR, "div[role='textbox'][contenteditable='true']")
                caption_area2.click()
                tiny_sleep(0.5, 1.0)
                caption_area2.send_keys(CAPTION)
            except Exception:
                print("⚠️ Couldn't find caption textarea. Continuing without caption.")

        tiny_sleep(1, 1.8)

        # ---- SHARE / POST ----
        try:
            share_btn = wait.until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//button[.//div[text()='Share']] | //div[text()='Share' or .='Share'] | //button[contains(., 'Share')]")
                )
            )
            tiny_sleep()
            share_btn.click()
        except Exception:
            # Try alternative: a button with type=submit
            try:
                submit_btn = driver.find_element(By.XPATH, "//button[@type='button' and (contains(., 'Share') or contains(., 'Publish'))]")
                submit_btn.click()
            except Exception:
                print("❌ Could not find Share button. Post likely failed.")
                driver.quit()
                return

        # ---- WAIT FOR POST TO COMPLETE ----
        # Wait until we see URL change or a success toast - fallback to checking that create page is gone
        time_started = time.time()
        success = False
        while time.time() - time_started < 20:
            tiny_sleep(0.5, 1.0)
            # If we are redirected to home or the create URL disappears, assume success
            if "/create" not in driver.current_url:
                success = True
                break

        if success:
            print("✅ One picture posted successfully!")
        else:
            print("⚠️ Posting may not have completed. Check the browser for errors.")

        tiny_sleep(2, 4)

    except Exception as e:
        print("❌ An exception occurred:", str(e))
    finally:
        try:
            driver.quit()
        except Exception:
            pass

if __name__ == "__main__":
    main()
