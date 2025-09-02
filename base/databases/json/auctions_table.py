import json
import os.path
from pathlib import Path
from leilao.base.databases.json.table import Table


class AuctionsTable(Table):
    def __init__(self):
        super().__init__()
        self.table = Path(self.get_json_path())

        if not self.table.exists():
            self.create_table()

    def create_table(self):
        with open(self.table, "w", encoding="utf-8") as auction_t:
            auction_t.write(json.dumps([{"auction_index": 0}]))

    def get_json_path(self):
        self.config_parser.read(os.path.join(os.path.dirname(__file__), "config", "config.ini"))
        auctions_table = self.config_parser.get("paths", "auction_history_table")

        return os.path.join(os.path.dirname(__file__), auctions_table)

    def write_in_table(self, dict_list: list):
        with open(self.table, "w", encoding= "utf-8") as auction_t:
            auction_t.write(json.dumps(dict_list, indent= 5))

    def read_table(self) -> list[dict]:
        with open(self.table, "r", encoding= "utf-8") as auction_t:
            dict_list = json.load(auction_t)

        return dict_list
