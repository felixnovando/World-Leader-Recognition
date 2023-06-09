from bs4 import BeautifulSoup as bs
import requests
from dotenv import load_dotenv
import os

load_dotenv()
URL = os.getenv("TARGET_URL")

def get_all_label():
    req = requests.get(URL)
    soup = bs(req.content, 'html.parser')
    names = soup.select(".name")
    names = [name.get_text() for name in names]
    return names


def get_assets():
    ids = [1, 2, 3, 4, 5, 6, 7, 8]
    images_url = []
    labels = []

    for idx, id in enumerate(ids):
        final_url = URL + f"/pages/photos.php?id={id}"
        req = requests.get(final_url)
        soup = bs(req.content, 'html.parser')
        paths = soup.select("img")
        for path in paths:
            images_url.append(URL + path['src'][2:])
            #starting from 0
            labels.append(id-1)

    return images_url, labels

def get_final_photo():
    req = requests.get(URL + "/pages/peoples.php")
    soup = bs(req.content, 'html.parser')
    images = soup.select("img")
    images_url = [URL + image["src"][2:] for image in images]
    return images_url