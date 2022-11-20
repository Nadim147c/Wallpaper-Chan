from datetime import datetime
from tkinter import filedialog
from pystray import Menu, MenuItem, Icon
from bs4 import BeautifulSoup
from glob import glob
from PIL import Image
from threading import Thread
import shutil
import subprocess
import json
import os
import random
import re
import time
import ctypes
import requests
import hashlib
import winreg


class Config:
    def __init__(
        self, auto_change, auto_change_time, auto_change_source, theme, color, filters
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

            if re.search(regex, title, re.IGNORECASE):
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


def set_filters(text, config):
    inputs = text.get(1.0, "end-1c")
    filters = re.sub("( *,( |\n)*|\n ?)+", ",", inputs).split(",")
    filters = list(filter(lambda str: len(str) > 0, filters))
    config.filters = filters
    config.save()


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


"""

def reset():
    ctypes.windll.user32.SystemParametersInfoW(
        20, 0, os.path.abspath("assets/default.jpg"), 0)


def stop():
    icon.stop()


def get_time_string(): return str(datetime.now())


auto_change_string = get_time_string()


def auto_change_wallpaper(method, time):
    global auto_change_string

    timestr = get_time_string()
    auto_change_string = timestr

    while timestr == auto_change_string:
        if method == 1:
            set_from_library(False)
        elif method == 2:
            set_from_wallpaper_abyss()
        time.sleep(time)


def set_auto_changer(method, time):
    global auto_change
    if auto_change["method"] == method and auto_change["time"] == time:
        method = 0
    auto_change["time"] = time
    auto_change["method"] = method
    config["auto-change"] = auto_change
    with open("config.json", "w") as outfile:
        outfile.write(json.dumps(config, indent=4))
        outfile.close()


def set_auto_changer_checked(method, time):
    global auto_change
    if auto_change["method"] == method and auto_change["time"] == time:
        return True
    else:
        return False



icon_image = Image.open(icon_path)

icon = Icon("Wallpaper", icon_image,  title="Anime Wallpaper", menu=Menu(
    MenuItem("Set Random Wallpaper", Menu(
        MenuItem("Internet", lambda: Thread(
            target=set_from_wallpaper_abyss).start()),
        MenuItem("Library", set_from_library)
    )),
    MenuItem("Auto Change", Menu(
        MenuItem("Internet", Menu(
            MenuItem("Every Minute", action=lambda: set_auto_changer(
                2, 60), checked=lambda e: set_auto_changer_checked(2, 60),),
            MenuItem("Every 5 Minutes", action=lambda: set_auto_changer(
                2, 60 * 5), checked=lambda e: set_auto_changer_checked(2, 60 * 5),),
            MenuItem("Every 30 Minutes", action=lambda: set_auto_changer(
                2, 60 * 30), checked=lambda e: set_auto_changer_checked(2, 60 * 30),),
            MenuItem("Every Hour", action=lambda: set_auto_changer(
                2, 60 * 60), checked=lambda e: set_auto_changer_checked(2, 60*60),),
        )),
        MenuItem("Library", Menu(
            MenuItem("Every Minute", action=lambda: set_auto_changer(
                1, 60), checked=lambda e: set_auto_changer_checked(1, 60),),
            MenuItem("Every 5 Minutes", action=lambda: set_auto_changer(
                1, 60 * 5), checked=lambda e: set_auto_changer_checked(1, 60 * 5),),
            MenuItem("Every 30 Minutes", action=lambda: set_auto_changer(
                1, 60 * 30), checked=lambda e: set_auto_changer_checked(1, 60 * 30),),
            MenuItem("Every Hour", action=lambda: set_auto_changer(
                1, 60 * 60), checked=lambda e: set_auto_changer_checked(1, 60*60),),
        )),
    )),
    MenuItem("Open", Menu(
        MenuItem("Temporary", action=lambda: open_folder("temp")),
        MenuItem("Library", action=lambda: open_folder("library"))
    )),
    MenuItem("Settings", Menu(
        MenuItem("Notifications", toggle_notification,
                 checked=lambda i: notifications),
        MenuItem("Filters", set_filters)
    )),
    MenuItem("Add to Library", add_to_library),
    MenuItem("Reset Wallpaper", reset),
    MenuItem("Exit", stop),
))


"""
