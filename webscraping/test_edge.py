from selenium import webdriver
from selenium.webdriver.edge.service import Service

# Path to your downloaded msedgedriver.exe
driver_path = "C:/Drivers/msedgedriver.exe"
driver = webdriver.Edge(service=Service(driver_path))

driver.get("https://www.google.com")

print("Page Title:", driver.title)
driver.quit()
