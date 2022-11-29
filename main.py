from functions import set_random, folder, settings, auto_change, filters, config
from threading import Thread
from PIL import Image
from pystray import Icon, Menu, MenuItem
from os import path, chdir, mkdir
import customtkinter as ctk
import tkinter as tk
import ctypes.wintypes
import sys


buf = ctypes.create_unicode_buffer(ctypes.wintypes.MAX_PATH)
ctypes.windll.shell32.SHGetFolderPathW(None, 5, None, 0, buf)

documents = buf.value

app_dir = path.split(__file__)[0]
chdir(app_dir)


root_folder = path.join(documents, "Wallpaper Chan")
if not path.exists(root_folder):
    mkdir(root_folder)

library_folder = path.join(root_folder, "library")
if not path.exists(library_folder):
    mkdir(library_folder)

temporary_folder = path.join(root_folder, "temporary")
if not path.exists(temporary_folder):
    mkdir(temporary_folder)

cache_folder = path.join(root_folder, "cache")
if not path.exists(cache_folder):
    mkdir(cache_folder)

config_path = path.join(root_folder, "config.json")

config = config.Config.get_config(config_path)
app_life = True
get_app_life = lambda: app_life

ctk.set_appearance_mode(config.theme)
ctk.set_default_color_theme(config.color)

app = ctk.CTk()
app.title("Wallpaper Chan")
app.iconbitmap("assets/colored_main.ico")


def on_close():
    def destroy(exit_icon: bool = True):
        global app_life
        app_life = False
        app.destroy()
        if exit_icon:
            icon.stop()

    def open_app():
        app.iconify()
        app.deiconify()
        app.focus_force()
        icon.stop()

    app.withdraw()
    icon_image = Image.open("assets/colored_main.ico")
    icon = Icon(
        "Wallpaper Chan",
        icon_image,
        "Wallpaper Chan",
        menu=Menu(MenuItem("Open", open_app), MenuItem("Exit", destroy)),
    )

    if config.system_tray:
        icon.run()
    else:
        destroy(False)


app.protocol("WM_DELETE_WINDOW", on_close)

window_height = 620
window_width = 720
app.minsize(height=window_height, width=window_width)

screen_width = app.winfo_screenwidth()
screen_height = app.winfo_screenheight()

x = int((screen_width / 2) - (window_width / 2))
y = int((screen_height / 2) - (window_height / 2))

app.geometry(f"{window_width}x{window_height}+{x}+{y}")

app.grid_rowconfigure(0, weight=1)
app.grid_columnconfigure(1, weight=1)


left_frame = ctk.CTkFrame(master=app, corner_radius=0)
left_frame.grid(row=0, sticky="nsw", pady=0)

left_frame.grid_columnconfigure(0, weight=1)
left_frame.grid_rowconfigure(3, weight=1)

right_frame = ctk.CTkFrame(master=app)
right_frame.grid(row=0, column=1, columnspan=2, sticky="nwse", pady=10, padx=10)

right_frame.grid_columnconfigure(0, weight=1)
right_frame.grid_rowconfigure(2, weight=1)

ctk.CTkLabel(
    master=left_frame, text="Wallpaper Chan", text_font=("Arial bold", -20)
).grid(row=0, pady=10, padx=10)


# Set random from:---

set_random_frame = ctk.CTkFrame(master=left_frame)
set_random_frame.grid(row=1, padx=10, pady=10, sticky="we")

set_random_frame.grid_columnconfigure(0, weight=1)


ctk.CTkLabel(
    master=set_random_frame, text="Set random from:", text_font=("Arial bold", -12)
).grid(row=0, pady=5, padx=5, sticky="we")

ctk.CTkButton(
    master=set_random_frame,
    text="Internet",
    command=lambda: set_random.set_from_wallpaper_abyss_with_progress(
        temporary_folder, cache_folder, config, app
    ),
).grid(row=1, pady=10, padx=5, sticky="we")

ctk.CTkButton(
    master=set_random_frame,
    text="Library",
    command=lambda: Thread(
        target=lambda: set_random.set_from_library(library_folder, True)
    ).start(),
).grid(row=2, pady=10, padx=5, sticky="we")


# Open folder:-

open_folder_frame = ctk.CTkFrame(master=left_frame)
open_folder_frame.grid(row=2, padx=10, pady=10, sticky="we")

open_folder_frame.grid_columnconfigure(0, weight=1)

ctk.CTkLabel(
    master=open_folder_frame, text="Open folder:", text_font=("Arial bold", -12)
).grid(row=0, pady=5, padx=5, sticky="we")

ctk.CTkButton(
    master=open_folder_frame,
    text="Library",
    command=lambda: folder.open_folder(library_folder),
).grid(row=1, pady=10, padx=5, sticky="we")

ctk.CTkButton(
    master=open_folder_frame,
    text="Temporary",
    command=lambda: folder.open_folder(temporary_folder),
).grid(row=2, pady=10, padx=5, sticky="we")

ctk.CTkButton(
    master=open_folder_frame,
    text="Cache",
    command=lambda: folder.open_folder(cache_folder),
).grid(row=3, pady=10, padx=5, sticky="we")


# Settings

ctk.CTkLabel(master=left_frame, text="Settings:", text_font=("Arial bold", -12)).grid(
    row=3,
    sticky="wes",
)

run_on_start = ctk.CTkSwitch(
    master=left_frame,
    text="Run on startup",
    command=lambda: settings.set_startup_registry(app_dir, run_on_start.check_state),
)
run_on_start.grid(row=4, sticky="wes", padx=10, pady=3)
if settings.check_startup_registry():
    run_on_start.select()

exit_to_system_tray = ctk.CTkSwitch(
    master=left_frame,
    text="Stay on system tray",
    command=lambda: settings.toggle_system_tray(
        config, exit_to_system_tray.check_state
    ),
)
exit_to_system_tray.grid(row=6, sticky="wes", padx=10, pady=3)
if config.system_tray:
    exit_to_system_tray.select()


ctk.CTkButton(
    master=left_frame,
    text="Add to library",
    command=lambda: settings.add_to_library(app, temporary_folder, library_folder),
).grid(row=7, sticky="wes", pady=5, padx=10)


theme = ctk.CTkOptionMenu(
    master=left_frame,
    values=["System", "Light", "Dark"],
    command=lambda x: settings.change_theme(x, config, filtered_tag_frame),
)
theme.grid(row=8, sticky="wes", pady=5, padx=10)
theme.set("Theme")

color_change_warning = ctk.CTkLabel(
    master=left_frame,
    text="Restart the app!",
    text_font=("Arial bold", -8),
    text_color=["#800", "#a44"],
)


color = ctk.CTkOptionMenu(
    master=left_frame,
    values=["Green", "Blue", "Dark Blue"],
    command=lambda x: settings.change_color(config, x, color_change_warning),
)
color.grid(row=9, sticky="wes", pady=5, padx=10)
color.set("Color")


# Auto Change
auto_change_frame = ctk.CTkFrame(master=right_frame)
auto_change_frame.grid(row=0, sticky="wne", padx=10, pady=10)

auto_change_frame.grid_columnconfigure(0, weight=1)
auto_change_frame.grid_columnconfigure(1, weight=1)


ctk.CTkLabel(
    master=auto_change_frame,
    text="Auto change wallpaper:",
    text_font=("Arial bold", -12),
).grid(
    row=0,
    columnspan=2,
    sticky="we",
    pady=5,
    padx=5,
)

auto_change_switch = ctk.CTkSwitch(
    master=auto_change_frame,
    text="Auto change wallpaper",
    command=lambda: auto_change.toggle_auto_change(
        temporary_folder,
        library_folder,
        cache_folder,
        config,
        auto_change_switch,
        get_app_life,
    ),
)
auto_change_switch.grid(row=1, columnspan=2, sticky="we", padx=10)

if config.auto_change:
    auto_change_switch.toggle()


auto_change_source = ctk.CTkOptionMenu(
    master=auto_change_frame,
    values=["Internet", "Library"],
    command=lambda x: auto_change.set_auto_change_source(config, x),
)
auto_change_source.grid(row=2, pady=10, padx=5, sticky="we")
auto_change_source.set("Internet" if config.auto_change_source == 0 else "Library")


auto_change_time = ctk.CTkOptionMenu(
    master=auto_change_frame,
    values=[
        "Every minute",
        "Every 5 minutes",
        "Every 10 minutes",
        "Every 30 minutes",
        "Every hour",
        "Every 2 hours",
    ],
    command=lambda x: auto_change.set_auto_change_time(config, x),
)
auto_change_time.grid(row=2, column=1, pady=10, padx=5, sticky="we")

if config.auto_change_time == 60:
    auto_change_time.set("Every minute")
if config.auto_change_time == 300:
    auto_change_time.set("Every 5 minutes")
if config.auto_change_time == 600:
    auto_change_time.set("Every 10 minutes")
if config.auto_change_time == 1800:
    auto_change_time.set("Every 30 minutes")
if config.auto_change_time == 3600:
    auto_change_time.set("Every hour")
if config.auto_change_time == 7200:
    auto_change_time.set("Every 2 hours")


# Clear files
clear_wallpapers_frame = ctk.CTkFrame(master=right_frame)
clear_wallpapers_frame.grid(row=1, sticky="we", padx=10, pady=10)


clear_wallpapers_frame.grid_columnconfigure(0, weight=1)
clear_wallpapers_frame.grid_columnconfigure(1, weight=1)


ctk.CTkLabel(
    master=clear_wallpapers_frame,
    text="Clear files:",
    text_font=("Arial bold", -12),
).grid(
    row=0,
    columnspan=3,
    sticky="we",
    pady=5,
    padx=5,
)

ctk.CTkButton(
    master=clear_wallpapers_frame,
    text="Clear Temporary Wallpapers",
    fg_color=["#aaa", "#777"],
    hover_color=["#a44", "#800"],
    command=lambda: folder.clear_folder(temporary_folder, "temporary", app),
).grid(row=1, sticky="we", pady=5, padx=5)


ctk.CTkButton(
    master=clear_wallpapers_frame,
    text="Clear Library Wallpapers",
    fg_color=["#aaa", "#777"],
    hover_color=["#a44", "#800"],
    command=lambda: folder.clear_folder(library_folder, "library", app),
).grid(row=1, column=1, sticky="we", pady=5, padx=5)

ctk.CTkButton(
    master=clear_wallpapers_frame,
    text="Clear page cache",
    fg_color=["#aaa", "#777"],
    hover_color=["#a44", "#800"],
    command=lambda: folder.clear_folder(cache_folder, "cache", app),
).grid(row=1, column=2, sticky="we", pady=5, padx=5)


# filters

filters_frame = ctk.CTkFrame(master=right_frame)
filters_frame.grid(row=2, padx=10, pady=10, sticky="nwse")

filters_frame.grid_columnconfigure(0, weight=1)
filters_frame.grid_rowconfigure(1, weight=1)


ctk.CTkLabel(master=filters_frame, text="Filters:", text_font=("Arial bold", -12)).grid(
    row=0,
    columnspan=2,
    pady=5,
    padx=5,
)


filtered_tag_frame = tk.Frame(master=filters_frame)
filtered_tag_frame.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky="nwse")
filtered_tag_frame.configure(
    bg="#383838"
    if ctk.appearance_mode_tracker.AppearanceModeTracker.appearance_mode == 1
    else "#d1d1d1"
)


filtered_tag_frame.bind(
    "<Configure>",
    lambda x: Thread(
        target=lambda: filters.show_filters(app, filtered_tag_frame, config, True)
    ).start(),
)


filter_entry = ctk.CTkEntry(master=filters_frame)
filter_entry.grid(row=2, column=0, padx=10, sticky="we")


filter_entry.bind(
    "<Return>",
    lambda x: filters.add_filter(app, filtered_tag_frame, config, filter_entry.entry),
)

ctk.CTkButton(
    master=filters_frame,
    text="add",
    command=lambda: filters.add_filter(
        app, filtered_tag_frame, config, filter_entry.entry
    ),
).grid(row=2, column=1, sticky="we", pady=10, padx=10)

ctk.CTkLabel(
    master=filters_frame,
    text="Avoid downloading any wallpaper contain following words/phrase.",
    text_font=("Arial", -9),
).grid(row=4, columnspan=2, pady=0, padx=10)

if "-startup" in sys.argv:
    if config.system_tray:
        on_close()
    else:
        app.iconify()

app.mainloop()
