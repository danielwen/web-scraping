# Scraping logic
# Web Scraping optional lecture
# 15-112 Fall 2017
# Daniel Wen

import os
import json
import urllib.parse
import io
import re
import requests
from bs4 import BeautifulSoup
from PIL import Image


# Download and parse webpage (cache results)
def soupGet(cache, url, refresh):
    if not refresh and url in cache:
        text = cache[url]
    else:
        text = requests.get(url).text
        cache[url] = text
    soup = BeautifulSoup(text, "lxml")
    return soup


# Scrape price from product page
def getPrice(cache, mainUrl, product, refresh):
    url = urllib.parse.urljoin(mainUrl, product["url"])
    soup = soupGet(cache, url, refresh)
    p = soup.select("p.u-mt0")[0]
    regex = r"\$\d+"
    price = re.search(regex, p.text).group(0)
    product["price"] = price


# Download product image (cache results)
def getImage(product, refresh):
    url = "https:" + product["image_url"]
    filename = urllib.parse.quote(url[:100], safe="")
    if not refresh and os.path.isfile(filename):
        with open(filename, "rb") as f:
            product["image"] = Image.open(io.BytesIO(f.read()))
    else:
        response = requests.get(url)
        with open(filename, "wb") as f:
            f.write(response.content)
        product["image"] = Image.open(io.BytesIO(response.content))


# Get list of products (name, price, image)
def getProductsUsingCache(cache, refresh):
    products = []
    url = "https://www.warbyparker.com/eyeglasses/men"
    soup = soupGet(cache, url, refresh)
    selector = "a.c-gallery-frame-radio__image-link.u-w100p"
    limit = 6

    for a in soup.select(selector, limit=limit):
        product_url = a["href"]
        img = a.select("img")[0]
        h2 = a.parent.parent.parent.select("h2")[0]
        product = {
            "name" : h2.text,
            "url" : a["href"],
            "image_url" : img["srcset"].split(",")[0]
        }
        products.append(product)

    for product in products:
        getPrice(cache, url, product, refresh)
        getImage(product, refresh)

    return products


# Get list of products
def getProducts(refresh=False):
    cache = {}
    filename = "cache.json"
    if os.path.isfile(filename):
        with open(filename) as f:
            cache = json.loads(f.read())

    result = getProductsUsingCache(cache, refresh)

    with open(filename, "w") as f:
        f.write(json.dumps(cache))

    return result


def test():
    print(getProducts())


if __name__ == "__main__":
    test()