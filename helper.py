import requests
from bs4 import BeautifulSoup

url = "https://brainlox.com/courses/category/technical"  # Change to the URL you want

response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")

# Extract and print all class names
all_classes = set()
for tag in soup.find_all(True):  # Finds all tags
    if tag.get("class"):
        all_classes.update(tag.get("class"))  # Add class names to set

print("All class names found on the page:")
print(all_classes)
