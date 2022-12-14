from bs4 import BeautifulSoup
from glob import glob
from threading import Thread
from functions.config import Config
from tkinter.messagebox import showerror
import customtkinter as ctk
import random
import re
import ctypes
import win32con
import requests
import hashlib
import os


def set_from_wallpaper_abyss(temp_path: str, cache_path: str, config: Config):
    wallpapers = []

    while len(wallpapers) == 0:
        page = random.randint(1, 500)
        doc_path = f"{cache_path}/page{str(page)}.txt"

        if not os.path.exists(doc_path):
            htmlContent = requests.get(
                f"https://wall.alphacoders.com/by_category.php?id=3&name=Anime+Wallpapers&filter=4K+Ultra+HD&page={page}"
            ).text

            with open(doc_path, "w", encoding="utf-8") as file:
                file.write(htmlContent)
            text = htmlContent
        else:
            with open(doc_path, "rb") as file:
                text = file.read()

        soup = BeautifulSoup(text, "html.parser")

        thumb_containers = soup.find_all("div", attrs={"class": "thumb-container"})

        for container in thumb_containers:
            title = container.div.a["title"]
            regex = "|".join(config.filters)

            if not len(config.filters) == 0 and re.search(regex, title, re.IGNORECASE):
                continue

            url = container.div.a.picture.img["src"]
            wallpapers.append(f"{url}")

    url = random.choice(wallpapers)

    image = requests.get(url)

    hash_str = hashlib.md5(str(url).encode("utf-8")).hexdigest()
    path = f"{temp_path}/{hash_str}.jpg"

    with open(path, "wb") as file:
        file.write(image.content)

    set_wallpaper(path)


def set_from_wallpaper_abyss_with_progress(
    temp_path: str, cache_path: str, config: Config, app: ctk.CTk
):

    progress = ctk.CTkToplevel(master=app)
    progress.overrideredirect(True)

    window_height = 60
    window_width = 400

    screen_width = app.winfo_screenwidth()
    screen_height = app.winfo_screenheight()

    x = int((screen_width / 2) - (window_width / 2))
    y = int((screen_height / 2) - (window_height / 2))

    progress.geometry(f"{window_width}x{window_height}+{x}+{y}")

    progress_bar = ctk.CTkProgressBar(master=progress, width=350)
    progress_bar.pack(pady=10)

    label = ctk.CTkLabel(master=progress, text="Finding wallpaper...")
    label.pack(pady=5)
    progress_bar.set(0.1)

    def download():
        wallpapers = []

        chunk_size = 1024 * 2

        while len(wallpapers) == 0:
            page = random.randint(1, 500)

            doc_path = f"{cache_path}/page{str(page)}.txt"
            if not os.path.exists(doc_path):
                page_url = f"https://wall.alphacoders.com/by_category.php?id=3&name=Anime+Wallpapers&filter=4K+Ultra+HD&page={page}"

                htmlContent = requests.get(page_url, stream=True)

                average_size = 50000
                htmlContent.raise_for_status()

                with open(doc_path, "wb") as f:
                    for i, data in enumerate(
                        htmlContent.iter_content(chunk_size=chunk_size)
                    ):
                        downloaded = ((i + 1) * chunk_size) / average_size
                        progress_bar.set(downloaded)
                        label.set_text(f"Finding: {int(downloaded* 100)}%")
                        f.write(data)

            with open(doc_path, "rb") as f:
                text = f.read()

            soup = BeautifulSoup(text, "html.parser")

            thumb_containers = soup.find_all("div", attrs={"class": "thumb-container"})

            for container in thumb_containers:
                title = container.div.a["title"]
                regex = "|".join(config.filters)

                if not len(config.filters) == 0 and re.search(
                    regex, title, re.IGNORECASE
                ):
                    continue

                image_url = container.div.a.picture.img["src"]
                wallpapers.append(f"{image_url}")

        image_url = random.choice(wallpapers)

        image = requests.get(image_url, stream=True)

        total_size = int(image.headers["content-length"])

        hash_str = hashlib.md5(str(image_url).encode("utf-8")).hexdigest()
        path = f"{temp_path}/{hash_str}.jpg"

        image.raise_for_status()

        with open(path, "wb") as f:
            for i, data in enumerate(image.iter_content(chunk_size=chunk_size)):
                downloaded = ((i + 1) * chunk_size) / total_size
                progress_bar.set(downloaded)
                label.set_text(f"Downloaded: {int(downloaded* 100)}%")
                f.write(data)
        progress.destroy()

        set_wallpaper(path)

    progress.after(1000, Thread(target=download).start)
    progress.mainloop()


def set_from_library(library_path: str, error: bool = False):
    files = glob(f"{library_path}/*.jpg") + glob(f"{library_path}/*.png")
    if len(files) == 0:
        if error:
            showerror(
                title="Library is empty",
                message="Library folder is empty. Add some wallpaper to library!",
            )
        return
    file = random.choice(files)
    set_wallpaper(file)


def set_wallpaper(path):
    changed = win32con.SPIF_UPDATEINIFILE | win32con.SPIF_SENDCHANGE
    print(changed)
    ctypes.windll.user32.SystemParametersInfoW(
        win32con.SPI_SETDESKWALLPAPER, 0, os.path.abspath(path), changed
    )
