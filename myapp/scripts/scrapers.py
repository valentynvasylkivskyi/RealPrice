from bs4 import BeautifulSoup
import requests
from user_agent import generate_user_agent


def allo(link):
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

def rozetka(link):
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

def citrus(link):
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

def comfy(link):
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

def moyo(link):
    data_source = requests.get(link, headers={'User-Agent': generate_user_agent()})
    soup = BeautifulSoup(data_source.text, "html.parser")
    data = {}
    data['product_name'] = soup.find("div", class_="tovar_title")\
            .find("div", class_="tovar_title__wrapper")\
            .find("h1").text.lstrip().rstrip()

    price = soup.find("div", class_="actual-price").find("span", class_="actual-price-amount").text
    product_price = ''
    for i in price.encode("utf-8").decode('windows-1251'):
        if str(i).isnumeric():
            product_price += i
    data['product_price'] = int(product_price)

    data['product_image_link'] = soup.find("div", class_="tovarnew-mainimagecontainer active")\
        .find("img").get("src")

    return data

def makeup(link):
    data_source = requests.get(link, headers={'User-Agent': generate_user_agent()})
    soup = BeautifulSoup(data_source.text, "html.parser")
    data = {}
    data['product_name'] = soup.find("div", class_="product-item__name").text.lstrip().rstrip()

    price = soup.find("div", class_="product-item__price-wrap").find("span", class_="product-item__price").find("div").find("span", class_="rus").text
    product_price = ''
    for i in price.encode("utf-8").decode('windows-1251'):
        if str(i).isnumeric():
            product_price += i
    data['product_price'] = int(product_price)

    data['product_image_link'] = soup.find("div", class_="product-slider__item sl__i")\
        .find("img").get("src")

    return data

def foxtrot(link):
    data_source = requests.get(link, headers={'User-Agent': generate_user_agent()})
    soup = BeautifulSoup(data_source.text, "html.parser")
    data = {}
    data['product_name'] = soup.find("h1", class_="page__title").text.lstrip().rstrip()

    price = soup.find("div", class_="product-box__main-price__main product-box__main-price__main_promo").find("div", class_="card-price").text
    product_price = ''
    for i in price.encode("utf-8").decode('windows-1251'):
        if str(i).isnumeric():
            product_price += i
    data['product_price'] = int(product_price)

    data['product_image_link'] = soup.find("div", class_="product-img__carousel")\
        .find("img").get("src")
    return data

def epicentrk(link):
    data_source = requests.get(link, headers={'User-Agent': generate_user_agent()})
    soup = BeautifulSoup(data_source.text, "html.parser")
    data = {}
    data['product_name'] = soup.find("h1", class_="nc").text.lstrip().rstrip()

    price = soup.find("div", class_="factualPrice").find("span", class_="price-wrapper").text
    product_price = ''
    for i in price.encode("utf-8").decode('windows-1251'):
        if str(i).isnumeric():
            product_price += i
        elif str(i) == ',' or '.':
            break
    data['product_price'] = int(product_price)

    data['product_image_link'] = soup.find("div", class_="card-slider__top-wrapper")\
        .find("img").get("src")
    return data

def f(link):
    data_source = requests.get(link, headers={'User-Agent': generate_user_agent()})
    soup = BeautifulSoup(data_source.text, "html.parser")
    data = {}
    data['product_name'] = soup.find("div", class_="box box24 product_title_box")\
        .find("h1").text.lstrip().rstrip()

    price = soup.find("div", class_="main product_price_main_6905939").text
    product_price = ''
    for i in price.encode("utf-8").decode('windows-1251'):
        if str(i).isnumeric():
            product_price += i
    data['product_price'] = int(product_price)

    data['product_image_link'] = soup.find("div", class_="img_part_big")\
        .find("img").get("src")

    return data

def add(link):
    data_source = requests.get(link, headers={'User-Agent': generate_user_agent()})
    soup = BeautifulSoup(data_source.text, "html.parser")
    data = {}
    data['product_name'] = soup.find("div", class_="product-name pg-product-name-padding")\
        .find("h1").text.lstrip().rstrip()

    price = soup.find("span", class_="regular-price").find("span", class_="price").text
    product_price = ''
    for i in price.encode("utf-8").decode('windows-1251'):
        if str(i).isnumeric():
            product_price += i
        elif str(i) == ',' or '.':
            break
    data['product_price'] = int(product_price)

    data['product_image_link'] = soup.find("div", class_="product-image-gallery")\
        .find("img").get("data-src")

    return data

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






