from __future__ import annotations
from typing import TYPE_CHECKING
import customtkinter as ctk
import customtkinter as ctk
import subprocess
import os

if TYPE_CHECKING:
    from structures.left_frame import LeftFrame
    from structures.app import App


class OpenFolder:
    def __init__(self, root: App, parent: LeftFrame):
        self.root = root
        self.parent = parent

        self.frame = ctk.CTkFrame(master=parent.frame)
        self.frame.grid(row=2, padx=10, pady=10, sticky="we")

        self.frame.grid_columnconfigure(0, weight=1)

        self.title = ctk.CTkLabel(
            master=self.frame, text="Open folder:", text_font=("Arial bold", -12)
        )
        self.title.grid(row=0, pady=5, padx=5, sticky="we")

        self.library_button = ctk.CTkButton(
            master=self.frame,
            text="Library",
            command=lambda: self.open_folder(root.library_folder),
        )
        self.library_button.grid(row=1, pady=10, padx=5, sticky="we")

        self.temporary_button = ctk.CTkButton(
            master=self.frame,
            text="Temporary",
            command=lambda: self.open_folder(root.temporary_folder),
        )
        self.temporary_button.grid(row=2, pady=10, padx=5, sticky="we")

        self.cache_button = ctk.CTkButton(
            master=self.frame,
            text="Cache",
            command=lambda: self.open_folder(root.cache_folder),
        )
        self.cache_button.grid(row=3, pady=10, padx=5, sticky="we")

    def open_folder(self, path: str):
        FILEBROWSER_PATH = os.path.join(os.getenv("WINDIR"), "explorer.exe")
        path = os.path.normpath(path)
        subprocess.run([FILEBROWSER_PATH, path])
