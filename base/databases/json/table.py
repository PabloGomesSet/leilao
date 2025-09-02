from configparser import ConfigParser
from pathlib import Path


class Table:
    def __init__(self):
        self.config_parser = ConfigParser()

    def create_table(self):
        pass

    def get_json_path(self)-> Path:
        pass

    def write_in_table(self, dict_list: list):
        pass

    def read_table(self) -> list[dict]:
        pass