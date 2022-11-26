from functions.config import Config
from tkinter import Text
import customtkinter as ctk
import tkinter as tk
import time


def show_filters(
    app: ctk.CTk,
    filtered_tag_frame: ctk.CTkFrame,
    config: Config,
    configure: bool = False,
):
    width = app.winfo_width()
    height = app.winfo_height()

    if configure:
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

    rely_increase = 24 / filtered_tag_frame_height

    for i, tag in enumerate(config.filters):

        def get_button_function(i):
            def remove_filter():
                del config.filters[i]
                config.save()
                show_filters(app, filtered_tag_frame, config)

            return remove_filter

        remove_filter_function = get_button_function(i)

        cross = tk.PhotoImage(file="assets/cross.png")

        label = ctk.CTkButton(
            master=filtered_tag_frame,
            text=tag,
            image=cross,
            compound="right",
            text_font=("Arial Bold", -12),
            width=1,
            height=1,
        )

        label.configure(command=remove_filter_function)

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


def add_filter(
    app: ctk.CTk, filtered_tag_frame: ctk.CTkFrame, config: Config, text: Text
):
    text_content = text.get()
    text.delete(0, len(text_content))
    config.filters.append(text_content)
    config.save()
    show_filters(app, filtered_tag_frame, config)
