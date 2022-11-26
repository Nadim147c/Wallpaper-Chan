from functions import set_random
from functions.config import Config
from threading import Thread
import customtkinter as ctk
import time


def auto_change_wallpaper(
    temp_path: str, library_path: str, cache_path: str, config: Config, get_app_life
):
    auto_change_active_time = time.time()
    while config.auto_change and get_app_life():
        time.sleep(0.7)
        current_time = time.time()
        difference = current_time - auto_change_active_time
        if difference >= config.auto_change_time:
            if config.auto_change_source == 0:
                set_random.set_from_wallpaper_abyss(temp_path, cache_path, config)
            else:
                set_random.set_from_library(library_path)
            auto_change_active_time = current_time
        else:
            continue


def toggle_auto_change(
    temp_path: str,
    library_path: str,
    cache_path: str,
    config: Config,
    switch: ctk.CTkSwitch,
    get_app_life,
):
    config.auto_change = switch.check_state
    config.save()
    if config.auto_change:
        Thread(
            target=lambda: auto_change_wallpaper(
                temp_path, library_path, cache_path, config, get_app_life
            )
        ).start()


def set_auto_change_source(config: Config, name: str):
    config.auto_change_source = 0 if name == "Internet" else 1
    config.save()


def set_auto_change_time(config: Config, time: str):
    if time == "Every minute":
        time = 60
    elif time == "Every 5 minutes":
        time = 60 * 5
    elif time == "Every 10 minutes":
        time = 60 * 10
    elif time == "Every 30 minutes":
        time = 60 * 30
    elif time == "Every hour":
        time = 60 * 60
    else:
        time = 60 * 60 * 2

    config.auto_change_time = time
    config.save()
