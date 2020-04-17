from bs4 import BeautifulSoup
import requests
from user_agent import generate_user_agent


link = "https://comfy.ua/ua/smartfon-xiaomi-redmi-note-8-4-64gb-space-black.html"

def scrap_comfy(link):
    data_source = requests.get(link, headers={'User-Agent': generate_user_agent()})
    soup = BeautifulSoup(data_source.text, "html.parser")
    data = {}
    try:
        data['product_name'] = soup.find("div", class_="product-card-header")\
            .find("div", class_="product-card__right")\
            .find("h1").text.lstrip().rstrip()
    except:
            data['product_name'] = soup.find("div", class_="product-card-header")\
            .find("div", class_="product-card__left")\
            .find("div", class_="product-card__name").text.lstrip().rstrip()

    price = soup.find("div", class_="price-box__content-i").find("span", class_="price-value").text
    product_price = ''
    for i in price.encode("utf-8").decode('windows-1251'):
        if str(i).isnumeric():
            product_price += i
    data['product_price'] = int(product_price)

    data['product_image_link'] = soup.find("div", class_="gallery")\
        .find("ul", id="galleryList")\
        .find("li")\
        .find("img").get("src")

    return data

print(scrap_comfy(link))













