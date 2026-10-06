from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By
import time
import pandas as pd

# Edge WebDriver path
driver_path = "C:/Drivers/msedgedriver.exe"

# Launch Edge
driver = webdriver.Edge(service=Service(driver_path))
driver.maximize_window()

# Cars24 Maruti cars in Mumbai
url = "https://www.cars24.com/buy-used-maruti-cars-mumbai/"
driver.get(url)
time.sleep(5)  # wait for initial load

# Infinite scroll to load all cars
last_height = driver.execute_script("return document.body.scrollHeight")
while True:
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(3)
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height

# Find all car cards
cars = driver.find_elements(By.CSS_SELECTOR, "div._3F0A0")  # container for each car card

data = []
for car in cars:
    # Car title & variant
    try:
        full_title = car.find_element(By.CSS_SELECTOR, "h1.sc-braxZu.fjhfdl").text
        variant = car.find_element(By.CSS_SELECTOR, "h1.sc-braxZu.fjhfdl span.sc-braxZu.jxZIsY").text
        model = full_title.replace(variant, "").strip()
    except:
        full_title = model = variant = ""
    
    # Car details
    try:
        details = car.find_elements(By.CSS_SELECTOR, "div.styles_carMeta__hm1XQ p")
        km = details[0].text if len(details) > 0 else ""
        owner = details[1].text if len(details) > 1 else ""
        transmission = details[2].text if len(details) > 2 else ""
        fuel = details[3].text if len(details) > 3 else ""
        registration = details[4].text if len(details) > 4 else ""
    except:
        km = owner = transmission = fuel = registration = ""
    
    # Price
    try:
        price = car.find_element(By.CSS_SELECTOR, "h2._2QKgL").text
    except:
        price = ""
    
    # Location
    try:
        location = car.find_element(By.CSS_SELECTOR, "p._2I5Yx").text
    except:
        location = ""
    
    data.append({
        "Full Title": full_title,
        "Model": model,
        "Variant": variant,
        "KM Driven": km,
        "Owner": owner,
        "Transmission": transmission,
        "Fuel": fuel,
        "Registration": registration,
        "Price": price,
        "Location": location
    })

# Save to CSV
df = pd.DataFrame(data)
df.to_csv("maruti_suzuki_mumbai.csv", index=False, encoding="utf-8")

print("✅ Scraping complete. Data saved to maruti_suzuki_mumbai.csv")

driver.quit()
