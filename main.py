from threading import Thread
import customtkinter as ctk
import funcs as fn
import os


config = fn.Config.get_config()

if not os.path.exists("library"):
    os.mkdir("library")
if not os.path.exists("temp"):
    os.mkdir("temp")


ctk.set_appearance_mode(config.theme)
ctk.set_default_color_theme(config.color)

app = ctk.CTk()
app.title("Wallpaper Chan")

window_height = 600
window_width = 600

screen_width = app.winfo_screenwidth()
screen_height = app.winfo_screenheight()

x = int((screen_width / 2) - (window_width / 2))
y = int((screen_height / 2) - (window_height / 2))

app.geometry(f"{window_height}x{window_width}+{x}+{y}")

app.grid_rowconfigure(0, weight=1)
app.grid_columnconfigure(1, weight=1)


def button_function():
    print("button pressed")


left_frame = ctk.CTkFrame(master=app, corner_radius=0)
left_frame.grid(row=0, sticky="nsw", pady=0)

left_frame.grid_columnconfigure(0, weight=1)
left_frame.grid_rowconfigure(3, weight=1)

right_frame = ctk.CTkFrame(master=app)
right_frame.grid(row=0, column=1, columnspan=2, sticky="nwse", pady=10, padx=10)

right_frame.grid_columnconfigure(0, weight=1)
right_frame.grid_rowconfigure(2, weight=1)

ctk.CTkLabel(
    master=left_frame, text="Anime Wallpaper", text_font=("Arial bold", -20)
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
    command=lambda: Thread(target=lambda: fn.set_from_wallpaper_abyss(config)).start(),
).grid(row=1, pady=10, padx=5, sticky="we")

ctk.CTkButton(
    master=set_random_frame,
    text="Library",
    command=lambda: Thread(target=fn.set_from_library).start(),
).grid(row=2, pady=10, padx=5, sticky="we")


# Open folder:-

open_folder_frame = ctk.CTkFrame(master=left_frame)
open_folder_frame.grid(row=2, padx=10, pady=10, sticky="we")

open_folder_frame.grid_columnconfigure(0, weight=1)

ctk.CTkLabel(
    master=open_folder_frame, text="Open Folder:", text_font=("Arial bold", -12)
).grid(row=0, pady=5, padx=5, sticky="we")

ctk.CTkButton(
    master=open_folder_frame, text="Library", command=lambda: fn.open_folder("library")
).grid(row=1, pady=10, padx=5, sticky="we")

ctk.CTkButton(
    master=open_folder_frame, text="Temporary", command=lambda: fn.open_folder("temp")
).grid(row=2, pady=10, padx=5, sticky="we")


# Setting

ctk.CTkLabel(master=left_frame, text="Settings:", text_font=("Arial bold", -12)).grid(
    row=3,
    sticky="wes",
)

ctk.CTkButton(master=left_frame, text="Add to library", command=button_function).grid(
    row=4, sticky="wes", pady=5, padx=10
)

theme = ctk.CTkOptionMenu(master=left_frame, values=["System", "Light", "Dark"])
theme.grid(row=5, sticky="wes", pady=5, padx=10)

color = ctk.CTkOptionMenu(master=left_frame, values=["Green", "Blue", "Red"])
color.grid(row=6, sticky="wes", pady=5, padx=10)


# Auto Change
auto_change_frame = ctk.CTkFrame(master=right_frame)
auto_change_frame.grid(row=0, sticky="wne", padx=10, pady=10)

auto_change_frame.grid_columnconfigure(0, weight=1)
auto_change_frame.grid_columnconfigure(1, weight=1)

ctk.CTkLabel(
    master=auto_change_frame,
    text="Auto change Wallpaper:",
    text_font=("Arial bold", -12),
).grid(
    row=0,
    columnspan=2,
    sticky="we",
    pady=5,
    padx=5,
)

ctk.CTkSwitch(master=auto_change_frame, text="Auto change wallpaper").grid(
    row=1, columnspan=2, sticky="we", padx=10
)


auto_change_source = ctk.CTkOptionMenu(
    master=auto_change_frame, values=["Internet", "Library"]
)
auto_change_source.grid(row=2, pady=10, padx=5, sticky="we")
auto_change_source.set("Source")

auto_change_time = ctk.CTkOptionMenu(
    master=auto_change_frame,
    values=[
        "Every minute",
        "Every 5 minutes",
        "Every 10 minutes",
        "Every 30 minutes",
        "Every hour",
    ],
)
auto_change_time.grid(row=2, column=1, pady=10, padx=5, sticky="we")
auto_change_time.set("Time")

# Clear wallpaper
clear_wallpapers_frame = ctk.CTkFrame(master=right_frame)
clear_wallpapers_frame.grid(row=1, sticky="we", padx=10, pady=10)


clear_wallpapers_frame.grid_columnconfigure(0, weight=1)
clear_wallpapers_frame.grid_columnconfigure(1, weight=1)


ctk.CTkLabel(
    master=clear_wallpapers_frame,
    text="Clear wallpapers:",
    text_font=("Arial bold", -12),
).grid(
    row=0,
    columnspan=2,
    sticky="we",
    pady=5,
    padx=5,
)

ctk.CTkButton(
    master=clear_wallpapers_frame,
    text="Clear Temporary Wallpapers",
    fg_color="#888",
    hover_color="#800",
    command=button_function,
).grid(row=1, sticky="we", pady=5, padx=5)


ctk.CTkButton(
    master=clear_wallpapers_frame,
    text="Clear Library Wallpapers",
    fg_color="#888",
    hover_color="#800",
    command=button_function,
).grid(row=1, column=1, sticky="we", pady=5, padx=5)


# filters

filters_frame = ctk.CTkFrame(master=right_frame)
filters_frame.grid(row=2, padx=10, pady=10, sticky="nwse")

filters_frame.grid_columnconfigure(0, weight=1)
filters_frame.grid_rowconfigure(1, weight=1)

ctk.CTkLabel(master=filters_frame, text="Filters:", text_font=("Arial bold", -12)).grid(
    row=0,
    pady=5,
    padx=5,
)

filter_textbox = ctk.CTkTextbox(master=filters_frame, border_color="#00aa00")
filter_textbox.grid(row=1, sticky="nwse", padx=10)

ctk.CTkButton(master=filters_frame, text="Save", command=button_function).grid(
    row=2, column=0, columnspan=2, sticky="we", pady=10, padx=5
)

ctk.CTkLabel(
    master=filters_frame,
    text="Avoid downloading any wallpaper contain following words.",
    text_font=("Arial bold", -8),
).grid(row=10, columnspan=2, pady=0, padx=10)


app.mainloop()
