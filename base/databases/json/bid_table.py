import json
import os
from pathlib import Path
from leilao.base.databases.json.table import Table


class BidTable(Table):
    def __init__(self):
        super().__init__()
        self.table = Path(self.get_json_path())

        if not self.table.exists():
            self.create_table()

    def create_table(self):
        with open(self.table, "w", encoding= "utf-8") as db:
            db.write(json.dumps([{"bid_index": 0}]))

    def get_json_path(self):
        self.config_parser.read(os.path.join(os.path.dirname(__file__), "config", "config.ini"))
        table_path = self.config_parser.get("paths", "bid_table")

        return os.path.join(os.path.dirname(__file__), table_path)

    def write_in_table(self, dict_list: list):
        with open(self.table, "w", encoding="utf-8") as table:
            table.write(json.dumps(dict_list, indent= 5))

    def read_table(self) -> list[dict]:
        with open(self.table, "r", encoding="utf-8") as db:
            bid_table = json.load(db)

        return bid_table
