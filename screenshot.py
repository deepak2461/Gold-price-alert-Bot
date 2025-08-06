import os
import time
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

# Telegram bot credentials (set in GitHub Secrets)
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_IDS_STR = os.getenv("TELEGRAM_CHAT_IDS", "")
TELEGRAM_CHAT_IDs = [cid.strip() for cid in TELEGRAM_CHAT_IDS_STR.split(",") if cid.strip()]
# URL to capture
URL = "https://www.goodreturns.in/gold-rates/visakhapatnam.html"
SCROLL_TO_ELEMENT = "//h2[contains(text(),'Gold Rate in Visakhapatnam for Last 10 Days')]"  
SCROLL_BY_PIXELS = 500  # Adjust as needed
def take_screenshot():
    options = Options()
    options.add_argument("--headless")  # Run in headless mode
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get(URL)
    time.sleep(5)  # Wait for the page to load
    if SCROLL_TO_ELEMENT:
        try:
            element = driver.find_element(By.XPATH, SCROLL_TO_ELEMENT)
            driver.execute_script("arguments[0].scrollIntoView({ behavior: 'smooth', block: 'center' });", element)
            time.sleep(2)  # Allow scrolling to complete
        except Exception as e:
            print(f"Error finding element: {e}")

    elif SCROLL_BY_PIXELS:
        driver.execute_script(f"window.scrollBy(0, {SCROLL_BY_PIXELS});")
        time.sleep(2)

    screenshot_path = "screenshot.png"
    driver.save_screenshot(screenshot_path)
    driver.quit()
    return screenshot_path

# -====== For single Chat_ID -============
def send_to_telegram(image_path):
    with open(image_path, "rb") as file:
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendPhoto"
        data = {"chat_id": TELEGRAM_CHAT_ID, "caption": "Daily Screenshot"}
        files = {"photo": file}
        response = requests.post(url, data=data, files=files)
    return response.json()

#======== For multiple chat_ids ========
# def send_to_telegram(image_path):
#     for chat_id in TELEGRAM_CHAT_IDs:
#         with open(image_path, "rb") as file:
#             url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendPhoto"
#             data = {"chat_id": chat_id, "caption": "Daily Screenshot"}
#             files = {"photo": file}
#             response = requests.post(url, data=data, files=files)
#             #print(f"Sent to {chat_id}: {response.status_code}")
#     return response.json()

if __name__ == "__main__":
    screenshot = take_screenshot()
    response = send_to_telegram(screenshot)
    print(response)
