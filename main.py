from threading import Thread
import customtkinter as ctk
import tkinter as tk
import funcs as fn
import os
import time


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
    master=open_folder_frame, text="Open folder:", text_font=("Arial bold", -12)
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

ctk.CTkButton(
    master=left_frame, text="Add to library", command=lambda: fn.add_to_library(app)
).grid(row=4, sticky="wes", pady=5, padx=10)


def change_theme(theme):
    config.theme = theme
    config.save()
    ctk.set_appearance_mode(theme)
    mode = ctk.appearance_mode_tracker.AppearanceModeTracker.get_mode()
    if theme.lower() == "system":
        mode = (
            ctk.appearance_mode_tracker.AppearanceModeTracker.detect_appearance_mode()
        )
    filtered_tag_frame.configure(bg="#383838" if mode == 1 else "#d1d1d1")


theme = ctk.CTkOptionMenu(
    master=left_frame, values=["System", "Light", "Dark"], command=change_theme
)
theme.grid(row=5, sticky="wes", pady=5, padx=10)
theme.set("Theme")

color_change_warning = ctk.CTkLabel(
    master=left_frame,
    text="Restart the app!",
    text_font=("Arial bold", -8),
    text_color=["#800", "#a44"],
)


def change_color(color: str):
    color = "-".join(color.lower().split(" "))
    config.color = color
    config.save()
    ctk.set_default_color_theme(color)
    color_change_warning.grid(
        row=7,
        sticky="wes",
        pady=2,
    )


color = ctk.CTkOptionMenu(
    master=left_frame, values=["Green", "Blue", "Dark Blue"], command=change_color
)
color.grid(row=6, sticky="wes", pady=5, padx=10)
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
    fg_color=["#aaa", "#777"],
    hover_color=["#a44", "#800"],
    command=button_function,
).grid(row=1, sticky="we", pady=5, padx=5)


ctk.CTkButton(
    master=clear_wallpapers_frame,
    text="Clear Library Wallpapers",
    fg_color=["#aaa", "#777"],
    hover_color=["#a44", "#800"],
    command=button_function,
).grid(row=1, column=1, sticky="we", pady=5, padx=5)


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


filtered_tag_frame = tk.Frame(
    master=filters_frame,
)

filtered_tag_frame.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky="nwse")
filtered_tag_frame.configure(
    bg="#383838"
    if ctk.appearance_mode_tracker.AppearanceModeTracker.appearance_mode == 1
    else "#d1d1d1"
)


def remove_filter(i):
    del config.filters[i]
    config.save()
    show_filters()


def add_filter(text):
    text_content = text.get()
    text.delete(0, len(text_content))
    config.filters.append(text_content)
    config.save()
    show_filters()


def show_filters(*args):
    width = app.winfo_width()
    height = app.winfo_height()

    if not len(args) == 0:
        time.sleep(1)

    if not width == app.winfo_width():
        return
    elif not height == app.winfo_height():
        return

    for widgets in filtered_tag_frame.winfo_children():
        widgets.destroy()

    app.update()

    filtered_tag_frame_width = filtered_tag_frame.winfo_width()
    filtered_tag_frame_height = filtered_tag_frame.winfo_height()

    padx = 5 / filtered_tag_frame_width
    pady = 5 / filtered_tag_frame_height

    tag_x = 0
    tag_y = pady

    rely_increase = 30 / filtered_tag_frame_height

    for i, tag in enumerate(config.filters):
        label = ctk.CTkButton(
            master=filtered_tag_frame,
            text=tag,
            text_font=("Arial Bold", -12),
            corner_radius=10,
            command=lambda: remove_filter(i),
            width=1,
            height=1,
        )

        tag_x += padx

        label.place(relx=tag_x, rely=tag_y)

        filtered_tag_frame.update()

        relx_increase = label.winfo_width() / filtered_tag_frame_width

        tag_x += relx_increase

        if tag_x > 1:
            tag_y += rely_increase + pady
            tag_x = 0 + padx

            label.place(relx=tag_x, rely=tag_y)

            tag_x += relx_increase


filtered_tag_frame.bind(
    "<Configure>", lambda x: Thread(target=lambda: show_filters(x)).start()
)


filter_entry = ctk.CTkEntry(master=filters_frame, border_color="#0a0")
filter_entry.grid(row=2, column=0, padx=10, sticky="we")


filter_entry.bind("<Return>", lambda x: add_filter(filter_entry.entry))

ctk.CTkButton(
    master=filters_frame, text="add", command=lambda: add_filter(filter_entry.entry)
).grid(row=2, column=1, sticky="we", pady=10, padx=5)

ctk.CTkLabel(
    master=filters_frame,
    text="Avoid downloading any wallpaper contain following words/phrase.",
    text_font=("Arial", -9),
).grid(row=4, columnspan=2, pady=0, padx=10)


app.mainloop()
