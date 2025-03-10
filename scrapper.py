from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
import csv

# Set up Chrome options
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run in the background
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")

# Set up the Chrome WebDriver
service = Service("chromedriver.exe")  # Ensure chromedriver.exe is in the same directory
driver = webdriver.Chrome(service=service, options=chrome_options)

# URL to scrape
url = "https://brainlox.com/courses/category/technical"
driver.get(url)
time.sleep(5)  # Wait for JavaScript to load

# Extract all course boxes
courses = driver.find_elements(By.CLASS_NAME, "single-courses-box")  # This contains each course

course_data = []

for course in courses:
    try:
        # Extract the course title
        title = course.find_element(By.CLASS_NAME, "courses-content").find_element(By.TAG_NAME, "h3").text
    except:
        title = "N/A"

    try:
        # Extract course description (if available inside courses-content)
        description = course.find_element(By.CLASS_NAME, "courses-content").find_element(By.TAG_NAME, "p").text
    except:
        description = "N/A"

    try:
        # Extract price
        price = course.find_element(By.CLASS_NAME, "price").text
    except:
        price = "Free"  # Assume free if no price found

    try:
        # Extract course link
        link = course.find_element(By.TAG_NAME, "a").get_attribute("href")
    except:
        link = "N/A"

    course_data.append([title, description, price, link])

# Save data to CSV
with open("brainlox_courses.csv", "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["Title", "Description", "Price", "Link"])
    writer.writerows(course_data)

print("✅ Scraping complete! Data saved to brainlox_courses.csv")

driver.quit()
