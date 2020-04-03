
# TEST
import os
from bs4 import BeautifulSoup
import requests
import wget


dir = os.path.abspath(os.path.dirname(__file__))
download_path = r'C:\Users\vasilkovskiy\Downloads\images'

url = "https://www.citrus.ua/noutbuki-i-ultrabuki/acer-swift-1-sf114-32-nxh1yeu014-obsidian-black-648948.html"


data_source = requests.get(url)
soup = BeautifulSoup(data_source.text, "html.parser")

# get product fields
product_name = soup.find("header", class_="product__header").find("h1").text
print(product_name)

price = soup.find("div", class_="price").find("span").text
print(price)

image_source = requests.get(url+"?tab=photo")
soup = BeautifulSoup(image_source.text, "html.parser")
product_image_link = soup.find("ul", class_="gallery").find("li").find("img").get('src')

print(product_image_link)

filename = wget.download(product_image_link)
os.rename(filename, os.path.join(download_path, filename))
print("Done!")












