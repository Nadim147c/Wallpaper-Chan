from structures.app import App
from threading import Thread
from os import path, chdir
import customtkinter as ctk
import tkinter as tk


app_dir = path.split(__file__)[0]
chdir(app_dir)

root = App(app_dir)
app = root.app

root.start()

# right_frame = ctk.CTkFrame(master=app)
# right_frame.grid(row=0, column=1, columnspan=2, sticky="nwse", pady=10, padx=10)

# right_frame.grid_columnconfigure(0, weight=1)
# right_frame.grid_rowconfigure(2, weight=1)

# Set random from:---


# Open folder:-


# Settings


# # Auto Change
# auto_change_frame = ctk.CTkFrame(master=right_frame)
# auto_change_frame.grid(row=0, sticky="wne", padx=10, pady=10)

# auto_change_frame.grid_columnconfigure(0, weight=1)
# auto_change_frame.grid_columnconfigure(1, weight=1)


# ctk.CTkLabel(
#     master=auto_change_frame,
#     text="Auto change wallpaper:",
#     text_font=("Arial bold", -12),
# ).grid(
#     row=0,
#     columnspan=2,
#     sticky="we",
#     pady=5,
#     padx=5,
# )

# auto_change_switch = ctk.CTkSwitch(
#     master=auto_change_frame,
#     text="Auto change wallpaper",
#     command=lambda: auto_change.toggle_auto_change(
#         temporary_folder,
#         library_folder,
#         cache_folder,
#         config,
#         auto_change_switch,
#         get_app_life,
#     ),
# )
# auto_change_switch.grid(row=1, columnspan=2, sticky="we", padx=10)

# if config.auto_change:
#     auto_change_switch.toggle()


# auto_change_source = ctk.CTkOptionMenu(
#     master=auto_change_frame,
#     values=["Internet", "Library"],
#     command=lambda x: auto_change.set_auto_change_source(config, x),
# )
# auto_change_source.grid(row=2, pady=10, padx=5, sticky="we")
# auto_change_source.set("Internet" if config.auto_change_source == 0 else "Library")


# auto_change_time = ctk.CTkOptionMenu(
#     master=auto_change_frame,
#     values=[
#         "Every minute",
#         "Every 5 minutes",
#         "Every 10 minutes",
#         "Every 30 minutes",
#         "Every hour",
#         "Every 2 hours",
#     ],
#     command=lambda x: auto_change.set_auto_change_time(config, x),
# )
# auto_change_time.grid(row=2, column=1, pady=10, padx=5, sticky="we")

# if config.auto_change_time == 60:
#     auto_change_time.set("Every minute")
# if config.auto_change_time == 300:
#     auto_change_time.set("Every 5 minutes")
# if config.auto_change_time == 600:
#     auto_change_time.set("Every 10 minutes")
# if config.auto_change_time == 1800:
#     auto_change_time.set("Every 30 minutes")
# if config.auto_change_time == 3600:
#     auto_change_time.set("Every hour")
# if config.auto_change_time == 7200:
#     auto_change_time.set("Every 2 hours")


# # Clear files
# clear_wallpapers_frame = ctk.CTkFrame(master=right_frame)
# clear_wallpapers_frame.grid(row=1, sticky="we", padx=10, pady=10)


# clear_wallpapers_frame.grid_columnconfigure(0, weight=1)
# clear_wallpapers_frame.grid_columnconfigure(1, weight=1)


# ctk.CTkLabel(
#     master=clear_wallpapers_frame,
#     text="Clear files:",
#     text_font=("Arial bold", -12),
# ).grid(
#     row=0,
#     columnspan=3,
#     sticky="we",
#     pady=5,
#     padx=5,
# )

# ctk.CTkButton(
#     master=clear_wallpapers_frame,
#     text="Clear Temporary Wallpapers",
#     fg_color=["#aaa", "#777"],
#     hover_color=["#a44", "#800"],
#     command=lambda: folder.clear_folder(temporary_folder, "temporary", app),
# ).grid(row=1, sticky="we", pady=5, padx=5)


# ctk.CTkButton(
#     master=clear_wallpapers_frame,
#     text="Clear Library Wallpapers",
#     fg_color=["#aaa", "#777"],
#     hover_color=["#a44", "#800"],
#     command=lambda: folder.clear_folder(library_folder, "library", app),
# ).grid(row=1, column=1, sticky="we", pady=5, padx=5)

# ctk.CTkButton(
#     master=clear_wallpapers_frame,
#     text="Clear page cache",
#     fg_color=["#aaa", "#777"],
#     hover_color=["#a44", "#800"],
#     command=lambda: folder.clear_folder(cache_folder, "cache", app),
# ).grid(row=1, column=2, sticky="we", pady=5, padx=5)


# # filters

# filters_frame = ctk.CTkFrame(master=right_frame)
# filters_frame.grid(row=2, padx=10, pady=10, sticky="nwse")

# filters_frame.grid_columnconfigure(0, weight=1)
# filters_frame.grid_rowconfigure(1, weight=1)


# ctk.CTkLabel(master=filters_frame, text="Filters:", text_font=("Arial bold", -12)).grid(
#     row=0,
#     columnspan=2,
#     pady=5,
#     padx=5,
# )


# filtered_tag_frame = tk.Frame(master=filters_frame)
# filtered_tag_frame.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky="nwse")
# filtered_tag_frame.configure(
#     bg="#383838"
#     if ctk.appearance_mode_tracker.AppearanceModeTracker.appearance_mode == 1
#     else "#d1d1d1"
# )


# filtered_tag_frame.bind(
#     "<Configure>",
#     lambda x: Thread(
#         target=lambda: filters.show_filters(app, filtered_tag_frame, config, True)
#     ).start(),
# )


# filter_entry = ctk.CTkEntry(master=filters_frame)
# filter_entry.grid(row=2, column=0, padx=10, sticky="we")


# filter_entry.bind(
#     "<Return>",
#     lambda x: filters.add_filter(app, filtered_tag_frame, config, filter_entry.entry),
# )

# ctk.CTkButton(
#     master=filters_frame,
#     text="add",
#     command=lambda: filters.add_filter(
#         app, filtered_tag_frame, config, filter_entry.entry
#     ),
# ).grid(row=2, column=1, sticky="we", pady=10, padx=10)

# ctk.CTkLabel(
#     master=filters_frame,
#     text="Avoid downloading any wallpaper contain following words/phrase.",
#     text_font=("Arial", -9),
# ).grid(row=4, columnspan=2, pady=0, padx=10)
