import requests
from bs4 import BeautifulSoup

url = "https://brainlox.com/courses/category/technical"  
response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")

all_classes = set()
for tag in soup.find_all(True):  
    if tag.get("class"):
        all_classes.update(tag.get("class"))  

print("All class names found on the page:")
print(all_classes)
