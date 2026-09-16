import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


def before_all(context):
    context.base_url = os.getenv("BASE_URL", "http://127.0.0.1:5000")
    context.wait_seconds = 5
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    context.driver = webdriver.Chrome(options=options)


def after_all(context):
    if getattr(context, "driver", None):
        context.driver.quit()
