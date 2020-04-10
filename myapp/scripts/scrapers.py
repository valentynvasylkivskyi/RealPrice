from bs4 import BeautifulSoup
import requests

# test --  remove after test
#from user_agent import generate_user_agent
#headers = {'User-Agent': generate_user_agent()}
#link = "https://allo.ua/ua/products/mobile/samsung-galaxy-s20-ultra-128gb-black-sm-g988bzkdsek.html"

def scrap_allo(link, headers):
    data_source = requests.get(link, headers)
    soup = BeautifulSoup(data_source.text, "html.parser")
    data = {}
    data['product_name'] = soup.find("div", class_="title-additional").find("h1").text.lstrip()
    price = soup.find("div", class_="price-box").find("span", class_="price").text
    product_price = ''
    for i in price.encode("utf-8").decode('windows-1251'):
        if str(i).isnumeric():
            product_price += i
    data['product_price'] = int(product_price)
    data['product_image_link'] = soup.find("img", id="image").get("src")

    return data





