import requests
from bs4 import BeautifulSoup

url = "https://www.walmart.com/reviews/product/10295756?entryPoint=viewAllReviewsTop"

response = requests.get(
    url,
    headers={
        "User-Agent":"Mozilla/5.0"
    }
)

soup = BeautifulSoup(
    response.text,
    "html.parser"
)

print(soup.title)

#Ran into problem - many websites like amazon, walmart, reddit etc require you to register through an API
# Can register now and wait for approval? In meantime there are public review datasets on kaggle - can work
# on clustering portion of project?