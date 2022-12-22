from __future__ import annotations
from typing import TYPE_CHECKING
from bs4 import BeautifulSoup
from glob import glob
from threading import Thread
from tkinter.messagebox import showerror
import customtkinter as ctk
import random
import re
import ctypes
import win32con
import requests
import hashlib
import os

if TYPE_CHECKING:
    from structures.left_frame import LeftFrame
    from structures.app import App


class SetRandom:
    def __init__(self, root: App, parent: LeftFrame):
        self.root = root
        self.parent = parent

        self.frame = ctk.CTkFrame(master=parent.frame)
        self.frame.grid(row=1, padx=10, pady=10, sticky="we")

        self.frame.grid_columnconfigure(0, weight=1)

        self.title = ctk.CTkLabel(
            master=self.frame, text="Set random from:", text_font=("Arial bold", -12)
        ).grid(row=0, pady=5, padx=5, sticky="we")

        self.internet_change = ctk.CTkButton(
            master=self.frame,
            text="Internet",
            command=self.set_from_wallpaper_abyss_with_progress,
        )
        self.internet_change.grid(row=1, pady=10, padx=5, sticky="we")

        self.library_change = ctk.CTkButton(
            master=self.frame,
            text="Library",
            command=Thread(target=lambda: self.set_from_library(True)).start,
        )
        self.library_change.grid(row=2, pady=10, padx=5, sticky="we")

    def set_from_wallpaper_abyss_with_progress(self):
        progress = ctk.CTkToplevel(master=self.root.app)
        progress.overrideredirect(True)

        window_height = 60
        window_width = 400

        screen_width = self.root.app.winfo_screenwidth()
        screen_height = self.root.app.winfo_screenheight()

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

                doc_path = f"{self.root.cache_folder}/page{str(page)}.txt"

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

                thumb_containers = soup.find_all(
                    "div", attrs={"class": "thumb-container"}
                )

                for container in thumb_containers:
                    title = container.div.a["title"]
                    regex = "|".join(self.root.config.filters)

                    if not len(self.root.config.filters) == 0 and re.search(
                        regex, title, re.IGNORECASE
                    ):
                        continue

                    image_url = container.div.a.picture.img["src"]
                    wallpapers.append(f"{image_url}")

            image_url = random.choice(wallpapers)

            image = requests.get(image_url, stream=True)

            total_size = int(image.headers["content-length"])

            hash_str = hashlib.md5(str(image_url).encode("utf-8")).hexdigest()
            path = f"{self.root.temporary_folder}/{hash_str}.jpg"

            image.raise_for_status()

            with open(path, "wb") as f:
                for i, data in enumerate(image.iter_content(chunk_size=chunk_size)):
                    downloaded = ((i + 1) * chunk_size) / total_size
                    progress_bar.set(downloaded)
                    label.set_text(f"Downloaded: {int(downloaded* 100)}%")
                    f.write(data)
            progress.destroy()

            self.set_wallpaper(path)

        progress.after(1000, Thread(target=download).start)
        progress.mainloop()

    def set_from_library(self, error: bool = False):
        path = self.root.library_folder
        files = glob(f"{path}/*.jpg") + glob(f"{path}/*.png")

        if len(files) == 0:
            return error and showerror(
                title="Library is empty",
                message="Library folder is empty. Add some wallpaper to library!",
            )

        file = random.choice(files)
        self.set_wallpaper(file)

    def set_wallpaper(self, path):
        changed = win32con.SPIF_UPDATEINIFILE | win32con.SPIF_SENDCHANGE
        ctypes.windll.user32.SystemParametersInfoW(
            win32con.SPI_SETDESKWALLPAPER, 0, os.path.abspath(path), changed
        )
