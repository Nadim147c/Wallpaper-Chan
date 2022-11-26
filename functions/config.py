import os
import json


class Config:
    def __init__(
        self,
        auto_change: bool,
        auto_change_time: int,
        auto_change_source: int,
        system_tray: bool,
        theme: str,
        color: str,
        filters: list[str],
        config_path: str,
    ):
        self.auto_change = auto_change
        self.auto_change_time = auto_change_time
        self.auto_change_source = auto_change_source
        self.system_tray = system_tray
        self.theme = theme
        self.color = color
        self.filters = filters
        self.config_path = config_path

    def get_config(config_path):
        if os.path.exists(config_path):
            with open(config_path, "r") as open_file:
                config = json.loads(open_file.read())

        else:
            config = {
                "auto_change": False,
                "auto_change_time": 60,
                "auto_change_source": 0,
                "system_tray": True,
                "theme": "system",
                "color": "green",
                "filters": [],
            }
            with open(config_path, "w") as outfile:
                outfile.write(json.dumps(config, indent=4))

        config["config_path"] = config_path

        return Config(**config)

    def save(self):
        path = self.config_path
        del self.config_path
        with open(path, "w") as outfile:
            outfile.write(json.dumps(self.__dict__, indent=4))
        self.config_path = path

    def __repr__(self) -> str:
        return "<Configuration>"
