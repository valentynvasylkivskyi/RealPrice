from bs4 import BeautifulSoup
import requests
from user_agent import generate_user_agent

link = "https://eva.ua/ua/pr11121/"

def eva(link):
    data_source = requests.get(link, headers={'User-Agent': generate_user_agent()})
    soup = BeautifulSoup(data_source.text, "html.parser")
    data = {}
    data['product_name'] = soup.find("div", class_="page-title-wrapper product")\
        .find("h1").text.lstrip().rstrip()

    price = soup.find("span", class_="price").text

    product_price = ''
    for i in price.encode("utf-8").decode('windows-1251'):
        if str(i).isnumeric():
            product_price += i
        elif str(i) == ',' or '.':
            break
    data['product_price'] = int(product_price)

    data['product_image_link'] = soup.find("div", class_="fotorama__stage__frame fotorama_vertical_ratio fotorama__loaded fotorama__loaded--img fotorama__active")
        #.find("img", class_="fotorama__img")
    return data

print(eva(link))













