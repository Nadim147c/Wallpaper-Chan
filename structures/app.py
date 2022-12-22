from structures.config import Config
from structures.left_frame import LeftFrame
from pystray import Icon, Menu, MenuItem
from PIL import Image
import customtkinter as ctk
import ctypes
import sys
import os


class App:
    def __init__(self, app_dir: str):
        self.title = "Wallpaper Chan"
        self.app_dir = app_dir
        self.app_path = os.path.join(self.app_dir, f"{self.title}.exe")

        self.app = ctk.CTk()
        self.app.title(self.title)
        self.app.iconbitmap("assets/colored_main.ico")
        self.app.protocol("WM_DELETE_WINDOW", self.on_close)
        self.set_window_size(620, 720)
        self.active = True

        self.icon = Icon(
            self.title,
            Image.open("assets/colored_main.ico"),
            self.title,
            menu=Menu(
                MenuItem("Open", self.open_app),
                MenuItem("Exit", self.destroy),
            ),
        )

        self.docs_path = self.get_docs_path()
        self.config_path = os.path.join(self.docs_path, "config.json")
        self.config = Config.get_config(self.config_path)

        ctk.set_appearance_mode(self.config.theme)
        ctk.set_default_color_theme(self.config.color)

        self.library_folder = self.get_directory("library")
        self.temporary_folder = self.get_directory("temporary")
        self.cache_folder = self.get_directory("cache")

        self.app.grid_rowconfigure(0, weight=1)
        self.app.grid_columnconfigure(1, weight=1)

        self.LeftFrame = LeftFrame(self)

    def start(self):
        if "-startup" in sys.argv:
            self.minimize()

        self.app.mainloop()

    def get_directory(self, name: str):
        path = os.path.join(self.docs_path, self.title, name)
        if not os.path.exists(path):
            os.mkdir(path)
        return path

    def get_docs_path(self):
        buf = ctypes.create_unicode_buffer(ctypes.wintypes.MAX_PATH)
        ctypes.windll.shell32.SHGetFolderPathW(None, 5, None, 0, buf)
        return buf.value

    def destroy(self, exit_icon: bool = True):
        self.active = False
        self.app.destroy()
        if exit_icon:
            self.icon.stop()

    def minimize(self):
        if self.config.system_tray:
            self.app.withdraw()
            self.icon.run()
        else:
            self.app.iconify()

    def open_app(self):
        self.app.iconify()
        self.app.deiconify()
        self.app.focus_force()
        self.icon.stop()

    def on_close(self):
        if self.config.system_tray:
            self.app.withdraw()
            self.icon.run()
        else:
            self.destroy(False)

    def set_window_size(self, height: int, width: int):
        window_height = height
        window_width = width
        self.app.minsize(height=window_height, width=window_width)

        screen_width = self.app.winfo_screenwidth()
        screen_height = self.app.winfo_screenheight()

        x = int((screen_width / 2) - (window_width / 2))
        y = int((screen_height / 2) - (window_height / 2))

        self.app.geometry(f"{window_width}x{window_height}+{x}+{y}")

    def __repr__(self) -> str:
        return f"<App:{self.app.title}>"
