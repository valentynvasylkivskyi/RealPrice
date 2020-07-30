from bs4 import BeautifulSoup
import requests
from user_agent import generate_user_agent

link = "https://agro-market.net/catalog/item/klen_veernyy_feniks_acer_palmatum_phoenix_konteyner_p9/"

def agro_market(link):
    data_source = requests.get(link, headers={'User-Agent': generate_user_agent()})
    soup = BeautifulSoup(data_source.text, "html.parser")
    data = {}
    data['product_name'] = soup.find("h1", class_="title_product").text.lstrip().rstrip()

    price = soup.find("span", class_="current-price").find("span").text
    product_price = ''
    for i in price.encode("utf-8").decode('windows-1251'):
        if str(i).isnumeric():
            product_price += i
        elif str(i) == ',' or '.':
            break
    data['product_price'] = int(product_price)

    data['product_image_link'] = "https://agro-market.net" + soup.find("span", rel="gallery")\
        .find("img").get("src")

    return data

print(agro_market(link))













