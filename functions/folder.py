from glob import glob
from tkinter.messagebox import askyesno
import customtkinter as ctk
import subprocess
import os


def open_folder(path: str):
    FILEBROWSER_PATH = os.path.join(os.getenv("WINDIR"), "explorer.exe")
    path = os.path.normpath(path)
    subprocess.run([FILEBROWSER_PATH, path])


def clear_folder(path: str, name: str, app: ctk.CTk):
    confirm = askyesno(
        f"Clear {name} files",
        f"All files in the {name} folder will be permanently delete. Do you want to delete them?",
    )
    if confirm:
        files = glob(f"{path}/*.jpg") + glob(f"{path}/*.png") + glob(f"{path}/*.txt")
        for file in files:
            os.remove(file)
