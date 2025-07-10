import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
import json

headers = {"User-Agent": "Mozilla/5.0"}

def scrape_design_info():
    url = "https://www.designinfo.in/?s=refractor+telescopes&post_type=product&dgwt_wcas=1"
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")

    products = []
    for product in soup.select("li.product"):
        title = product.h2.text.strip()
        price = product.select_one(".woocommerce-Price-amount").text.strip()
        link = product.a["href"]
        img = product.select_one("img")["src"]
        products.append({
            "title": title,
            "price": price,
            "source": "Design Info",
            "link": link,
            "image": img
        })
    return products

def scrape_modern_telescopes():
    options = Options()
    options.add_argument("--headless")  # Don't show browser window
    options.add_argument("--disable-gpu")
    driver = webdriver.Chrome(options=options)

    url = "https://moderntelescopes.net/collections/refractor"
    driver.get(url)
     # Wait up to 15 seconds for product items to be present
    try:
        WebDriverWait(driver, 15).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "boost-sd__product-item"))
        )
    except:
        print("Timed out waiting for products to load.")
        driver.quit()
        return []

    products = []
    items = driver.find_elements(By.CLASS_NAME, "boost-sd__product-item")
    for item in items:
        try:
            title = item.find_element(By.CLASS_NAME, "boost-sd__product-title").text.strip()
            price = item.find_element(By.CLASS_NAME, "boost-sd__product-price").text.strip()
            link = item.find_element(By.TAG_NAME, "a").get_attribute("href")
            img = item.find_element(By.TAG_NAME, "img").get_attribute("src")

            products.append({
                "title": title,
                "price": price,
                "source": "Modern Telescopes",
                "link": link,
                "image": img
            })
        except Exception as e:
            print("Error scraping a product:", e)

    driver.quit()
    return products

all_products = scrape_design_info() + scrape_modern_telescopes()

with open("data/telescopes.json", "w", encoding="utf-8") as f:
    json.dump(all_products, f, indent=2, ensure_ascii=False)

print(f"Saved {len(all_products)} products to 'telescopes.json'")

# design_products = scrape_design_info()
# print("Design Info Products:", len(design_products))
# for product in design_products:
#     print(product)
#     break  # remove break to see all

# modern_products = scrape_modern_telescopes()
# print("Modern Telescopes Products:", len(modern_products))
# for product in modern_products:
#     print(product)
#     break