from __future__ import annotations
from typing import TYPE_CHECKING
from structures.set_random import SetRandom
from structures.settings import Settings
from structures.open_folder import OpenFolder
import customtkinter as ctk

if TYPE_CHECKING:
    from structures.app import App


class LeftFrame:
    def __init__(self, root: App):
        self.root = root

        self.frame = ctk.CTkFrame(master=self.root.app, corner_radius=0)
        self.frame.grid(row=0, sticky="nsw", pady=0)

        self.frame.grid_columnconfigure(0, weight=1)
        self.frame.grid_rowconfigure(3, weight=1)

        self.title = ctk.CTkLabel(
            master=self.frame, text=root.title, text_font=("Arial bold", -20)
        )
        self.title.grid(row=0, pady=10, padx=10)

        self.SetRandom = SetRandom(root, self)
        self.Settings = Settings(root, self)
        self.OpenFolder = OpenFolder(root, self)
