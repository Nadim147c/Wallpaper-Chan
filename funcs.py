from tkinter import filedialog
from pystray import Menu, MenuItem, Icon
from bs4 import BeautifulSoup
from glob import glob
import shutil
import subprocess
import json
import os
import random
import re
import ctypes
import requests
import hashlib


class Config:
    def __init__(
        self,
        auto_change: bool,
        auto_change_time: int,
        auto_change_source: int,
        theme: str,
        color: str,
        filters: list[str],
    ):
        self.auto_change = auto_change
        self.auto_change_time = auto_change_time
        self.auto_change_source = auto_change_source
        self.theme = theme
        self.color = color
        self.filters = filters

    def get_config():
        if os.path.exists("config.json"):
            with open("config.json", "r") as open_file:
                config = json.loads(open_file.read())
                open_file.close()
        else:
            config = {
                "auto_change": True,
                "auto_change_time": 60,
                "auto_change_source": 0,
                "theme": "system",
                "color": "green",
                "filters": [],
            }
            with open("config.json", "w") as outfile:
                outfile.write(json.dumps(config, indent=4))
                outfile.close()

        return Config(**config)

    def save(self):
        with open("config.json", "w") as outfile:
            outfile.write(json.dumps(self.__dict__, indent=4))
            outfile.close()

    def __repr__(self) -> str:
        return "<Config>"


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


def open_folder(path):
    FILEBROWSER_PATH = os.path.join(os.getenv("WINDIR"), "explorer.exe")
    path = os.path.normpath(path)
    subprocess.run([FILEBROWSER_PATH, path])


def add_to_library(app):
    file_names = filedialog.askopenfilenames(
        title="Anime Wallpaper",
        initialdir="temp",
        filetypes=[("Image", r"*.jpg *.png")],
        parent=app,
    )

    for file in file_names:
        name = file.split("/")[-1]
        shutil.copy(src=file, dst=f"library/{name}")
