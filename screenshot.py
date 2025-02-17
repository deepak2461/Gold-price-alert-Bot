import os
import time
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

# Telegram bot credentials (set in GitHub Secrets)
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# URL to capture
URL = "https://github.com/deepak2461/dsc"

def take_screenshot():
    options = Options()
    options.add_argument("--headless")  # Run in headless mode
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get(URL)
    time.sleep(5)  # Wait for the page to load

    screenshot_path = "screenshot.png"
    driver.save_screenshot(screenshot_path)
    driver.quit()
    return screenshot_path

def send_to_telegram(image_path):
    with open(image_path, "rb") as file:
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendPhoto"
        data = {"chat_id": TELEGRAM_CHAT_ID, "caption": "Daily Screenshot"}
        files = {"photo": file}
        response = requests.post(url, data=data, files=files)
    return response.json()

if __name__ == "__main__":
    screenshot = take_screenshot()
    response = send_to_telegram(screenshot)
    print(response)
