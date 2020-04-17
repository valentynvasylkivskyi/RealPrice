from bs4 import BeautifulSoup
import requests
from user_agent import generate_user_agent


def scrap_allo(link):
    data_source = requests.get(link, headers={'User-Agent': generate_user_agent()})
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

def scrap_rozetka(link):
    data_source = requests.get(link, headers={'User-Agent': generate_user_agent()})
    soup = BeautifulSoup(data_source.text, "html.parser")
    data = {}
    data['product_name'] = soup.find("div", class_="product__heading").find("h1").text
    price = soup.find("div", class_="product-prices__inner").find_all("p")[0].text
    data['product_image_link'] = soup.find("figure", class_="product-photo__large-inner").find("img").get('src')

    product_price = ''
    for i in price.encode("utf-8").decode('windows-1251'):
        if str(i).isnumeric():
            product_price += i
    data['product_price'] = int(product_price)
    return data

def scrap_citrus(link):
    data_source = requests.get(link, headers={'User-Agent': generate_user_agent()})
    soup = BeautifulSoup(data_source.text, "html.parser")
    data = {}
    data['product_name'] = soup.find("header", class_="product__header").find("h1").text
    price = soup.find("div", class_="normal__prices").find_all("div")
    for i in price:
        if '<div class="price"' in str(i):
            price = i.find("span").text
    # get image source
    image_source = requests.get(link+"?tab=photo")
    soup = BeautifulSoup(image_source.text, "html.parser")
    data['product_image_link'] = soup.find("ul", class_="gallery").find("li").find("img").get('src')
    product_price = ''
    for i in price:
        if str(i).isnumeric():
            product_price += i
    data['product_price'] = int(product_price)
    return data

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







