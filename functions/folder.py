from glob import glob
import customtkinter as ctk
import subprocess
import os


def open_folder(path: str):
    FILEBROWSER_PATH = os.path.join(os.getenv("WINDIR"), "explorer.exe")
    path = os.path.normpath(path)
    subprocess.run([FILEBROWSER_PATH, path])


def clear_folder(path: str, app: ctk.CTk):
    warning = ctk.CTkToplevel(master=app)
    warning.title(f"Delete {path} wallpapers!")
    warning.iconbitmap("assets/colored_main.ico")

    window_height = 150
    window_width = 450

    screen_width = app.winfo_screenwidth()
    screen_height = app.winfo_screenheight()

    x = int((screen_width / 2) - (window_width / 2))
    y = int((screen_height / 2) - (window_height / 2))

    warning.geometry(f"{window_width}x{window_height}+{x}+{y}")

    warning.grid_rowconfigure(0, weight=1)
    warning.grid_columnconfigure(0, weight=1)

    ctk.CTkLabel(
        master=warning,
        text="You image will be deleted permanently. You can't restore them later!",
    ).grid(row=0, columnspan=3, padx=20, pady=20, sticky="nwse")

    def delete_files():
        files = glob(f"{path}/*.jpg") + glob(f"{path}/*.png") + glob(f"{path}/*.txt")
        for file in files:
            os.remove(file)
        warning.destroy()

    ctk.CTkButton(
        master=warning,
        text="Delete",
        fg_color=["#a44", "#800"],
        hover_color=["#800", "#a44"],
        command=delete_files,
    ).grid(row=1, column=1, padx=10, pady=10, sticky="e")

    ctk.CTkButton(
        master=warning,
        text="Cancel",
        fg_color=["#aaa", "#777"],
        hover_color=["#777", "#aaa"],
        command=warning.destroy,
    ).grid(row=1, column=2, padx=10, pady=10, sticky="e")

    warning.mainloop()
