from tkinter import filedialog
from functions.config import Config
import customtkinter as ctk
import shutil


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
