import os
import json


class Config:
    def __init__(
        self,
        auto_change: bool,
        auto_change_time: int,
        auto_change_source: int,
        theme: str,
        color: str,
        filters: list[str],
        minimized: bool,
        system_tray: bool,
    ):
        self.auto_change = auto_change
        self.auto_change_time = auto_change_time
        self.auto_change_source = auto_change_source
        self.theme = theme
        self.color = color
        self.filters = filters
        self.minimized = minimized
        self.system_tray = system_tray

    def get_config():
        if os.path.exists("config.json"):
            with open("config.json", "r") as open_file:
                config = json.loads(open_file.read())
                open_file.close()
        else:
            config = {
                "auto_change": False,
                "auto_change_time": 60,
                "auto_change_source": 0,
                "minimized": True,
                "system_tray": True,
                "theme": "system",
                "color": "green",
                "filters": [],
            }
            with open("config.json", "w") as outfile:
                outfile.write(json.dumps(config, indent=4))
                outfile.close()

        return Config(**config)

    def save(self):
        with open("config.json", "w") as outfile:
            outfile.write(json.dumps(self.__dict__, indent=4))
            outfile.close()

    def __repr__(self) -> str:
        return "<Config>"
