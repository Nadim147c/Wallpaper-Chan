from __future__ import annotations
from typing import TYPE_CHECKING
from tkinter import filedialog
import customtkinter as ctk
import winreg
import shutil

if TYPE_CHECKING:
    from structures.left_frame import LeftFrame
    from structures.app import App


class Settings:
    def __init__(self, root: App, parent: LeftFrame) -> None:
        self.root = root
        self.parent = parent

        self.title = ctk.CTkLabel(
            master=parent.frame, text="Settings:", text_font=("Arial bold", -12)
        )
        self.title.grid(row=3, sticky="wes")

        self.set_auto_start = ctk.CTkSwitch(
            master=parent.frame,
            text="Run on startup",
            command=self.set_startup_registry,
        )
        self.set_auto_start.grid(row=4, sticky="wes", padx=10, pady=3)

        if self.check_startup_registry():
            self.set_auto_start.select()

        self.exit_to_system_tray = ctk.CTkSwitch(
            master=parent.frame,
            text="Stay on system tray",
            command=self.toggle_system_tray,
        )

        self.exit_to_system_tray.grid(row=6, sticky="wes", padx=10, pady=3)
        if self.root.config.system_tray:
            self.exit_to_system_tray.select()

        self.add_to_library_button = ctk.CTkButton(
            master=parent.frame, text="Add to library", command=self.add_to_library
        )
        self.add_to_library_button.grid(row=7, sticky="wes", pady=5, padx=10)

        self.theme = ctk.CTkOptionMenu(
            master=parent.frame,
            values=["System", "Light", "Dark"],
            command=self.change_theme,
        )
        self.theme.grid(row=8, sticky="wes", pady=5, padx=10)
        self.theme.set("Theme")

        self.color_change_warning = ctk.CTkLabel(
            master=parent.frame,
            text="Restart the app!",
            text_font=("Arial bold", -8),
            text_color=["#800", "#a44"],
        )

        self.color = ctk.CTkOptionMenu(
            master=parent.frame,
            values=["Green", "Blue", "Dark Blue"],
            command=self.change_color,
        )
        self.color.grid(row=9, sticky="wes", pady=5, padx=10)
        self.color.set("Color")

    def add_to_library(self):
        file_names = filedialog.askopenfilenames(
            title=self.root.title,
            initialdir=self.root.temporary_folder,
            filetypes=[("Image", r"*.jpg *.png")],
            parent=self.root.app,
        )

        for file in file_names:
            name = file.split("/")[-1]
            shutil.copy(src=file, dst=f"{self.root.library_path}/{name}")

    def change_theme(self, theme: str):
        self.root.config.theme = theme
        self.root.config.save()
        ctk.set_appearance_mode(theme)

    def change_color(self, color: str):
        color = "-".join(color.lower().split(" "))
        self.root.config.color = color
        self.root.config.save()

        ctk.set_default_color_theme(color)

        self.color_change_warning.grid(row=10, sticky="wes", pady=2)

    def toggle_system_tray(self):
        self.root.config.system_tray = self.exit_to_system_tray.check_state
        self.root.config.save()

    def set_startup_registry(self):
        address = f'"{self.root.app_path}" -startup'
        autostart = self.set_auto_start.check_state

        with winreg.OpenKey(
            key=winreg.HKEY_CURRENT_USER,
            sub_key=r"Software\Microsoft\Windows\CurrentVersion\Run",
            reserved=0,
            access=winreg.KEY_ALL_ACCESS,
        ) as key:
            try:
                if autostart:
                    winreg.SetValueEx(key, self.root.title, 0, winreg.REG_SZ, address)
                else:
                    winreg.DeleteValue(key, self.root.title)
            except OSError:
                pass

    def check_startup_registry(self) -> bool:
        with winreg.OpenKey(
            key=winreg.HKEY_CURRENT_USER,
            sub_key=r"Software\Microsoft\Windows\CurrentVersion\Run",
            reserved=0,
            access=winreg.KEY_ALL_ACCESS,
        ) as key:
            idx = 0
            while idx < 1_000:  # Max 1.000 values
                try:
                    key_name, _, _ = winreg.EnumValue(key, idx)
                    if key_name == self.root.title:
                        return True
                    idx += 1
                except OSError:
                    break
        return False
