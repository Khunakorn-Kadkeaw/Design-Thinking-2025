import requests
from bs4 import BeautifulSoup

def scrape_gpu(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    
    products = []
    
    items = soup.select(".product-item")  # selector อาจต้องแก้
    
    for item in items:
        name = item.get_text(strip=True)
        products.append(name)
    
    return products
