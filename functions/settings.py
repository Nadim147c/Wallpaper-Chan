from tkinter import filedialog
from functions.config import Config
import customtkinter as ctk
import winreg
import shutil
import os


def add_to_library(app: ctk.CTk):
    file_names = filedialog.askopenfilenames(
        title="Wallpaper Chan",
        initialdir="temporary",
        filetypes=[("Image", r"*.jpg *.png")],
        parent=app,
    )

    for file in file_names:
        name = file.split("/")[-1]
        shutil.copy(src=file, dst=f"library/{name}")


def change_theme(theme: str, config: Config, filtered_tag_frame: ctk.CTkFrame):
    config.theme = theme
    config.save()
    ctk.set_appearance_mode(theme)
    mode = ctk.appearance_mode_tracker.AppearanceModeTracker.get_mode()
    if theme.lower() == "system":
        mode = (
            ctk.appearance_mode_tracker.AppearanceModeTracker.detect_appearance_mode()
        )
    filtered_tag_frame.configure(bg="#383838" if mode == 1 else "#d1d1d1")


def change_color(config: Config, color: str, color_change_warning: ctk.CTkLabel):
    color = "-".join(color.lower().split(" "))
    config.color = color
    config.save()
    ctk.set_default_color_theme(color)
    color_change_warning.grid(
        row=10,
        sticky="wes",
        pady=2,
    )


def toggle_minimized_start(config: Config, state: bool):
    config.minimized = state
    config.save()


def toggle_system_tray(config: Config, state: bool, minimized_start: ctk.CTkSwitch):
    config.system_tray = state
    if state:
        minimized_start.configure(state="normal")
    else:
        minimized_start.deselect()
        config.minimized = False
        minimized_start.configure(state="disabled")
    config.save()


def set_startup_registry(autostart: bool = True) -> bool:
    app_name = "Wallpaper Chan.exe"
    address = os.path.join(os.path.realpath(__file__), app_name)
    with winreg.OpenKey(
        key=winreg.HKEY_CURRENT_USER,
        sub_key=r"Software\Microsoft\Windows\CurrentVersion\Run",
        reserved=0,
        access=winreg.KEY_ALL_ACCESS,
    ) as key:
        try:
            if autostart:
                winreg.SetValueEx(key, app_name, 0, winreg.REG_SZ, address)
            else:
                winreg.DeleteValue(key, app_name)
        except OSError:
            pass


def check_startup_registry():
    app_name = "Wallpaper Chan.exe"

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
                if key_name == app_name:
                    return True
                idx += 1
            except OSError:
                break
    return False
