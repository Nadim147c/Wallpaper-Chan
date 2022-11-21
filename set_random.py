from bs4 import BeautifulSoup
from glob import glob
import random
import re
import ctypes
import requests
import hashlib
import os


def set_from_wallpaper_abyss(config):
    page = random.randint(1, 500)

    wallpapers = []

    while len(wallpapers) == 0:
        htmlContent = requests.get(
            f"https://wall.alphacoders.com/by_category.php?id=3&name=Anime+Wallpapers&filter=4K+Ultra+HD&page={page}"
        ).text

        soup = BeautifulSoup(htmlContent, "html.parser")

        thumb_containers = soup.find_all("div", attrs={"class": "thumb-container"})

        for container in thumb_containers:
            title = container.div.a["title"]
            regex = "|".join(config.filters)

            if not len(config.filters) == 0 and re.search(regex, title, re.IGNORECASE):
                continue

            url = container.div.a.picture.img["src"]
            wallpapers.append(f"{url}")

    image = requests.get(random.choice(wallpapers))

    hash_str = hashlib.md5(str(image.content).encode("utf-8")).hexdigest()
    path = f"temp/{hash_str}.jpg"

    with open(path, "wb") as file:
        file.write(image.content)
        file.close()

    ctypes.windll.user32.SystemParametersInfoW(20, 0, os.path.abspath(path), 0)


def set_from_library():
    files = glob("library/*.jpg") + glob("library/*.png")
    file = random.choice(files)
    ctypes.windll.user32.SystemParametersInfoW(20, 0, os.path.abspath(file), 0)
