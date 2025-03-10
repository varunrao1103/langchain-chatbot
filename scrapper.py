from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
import csv

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")

service = Service("chromedriver.exe")
driver = webdriver.Chrome(service=service, options=chrome_options)

url = "https://brainlox.com/courses/category/technical"
driver.get(url)
time.sleep(5)

courses = driver.find_elements(By.CLASS_NAME, "single-courses-box")

course_data = []

for course in courses:
    try:
        title = course.find_element(By.CLASS_NAME, "courses-content").find_element(By.TAG_NAME, "h3").text
    except:
        title = "N/A"

    try:
        description = course.find_element(By.CLASS_NAME, "courses-content").find_element(By.TAG_NAME, "p").text
    except:
        description = "N/A"

    try:
        price = course.find_element(By.CLASS_NAME, "price").text
    except:
        price = "Free"

    try:
        link = course.find_element(By.TAG_NAME, "a").get_attribute("href")
    except:
        link = "N/A"

    course_data.append([title, description, price, link])

with open("brainlox_courses.csv", "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["Title", "Description", "Price", "Link"])
    writer.writerows(course_data)

print("✅ Scraping complete! Data saved to brainlox_courses.csv")

driver.quit()
