from datetime import datetime
from operator import itemgetter
from zoneinfo import ZoneInfo
from leilao.base.databases.json.auctions_table import AuctionsTable


class Auction:
    def __init__(self, name: str):
        self.auction_index = self.set_index()
        self.auction_date = self.get_current_date()
        self.name = name
        self.status = True

    def get_last_index(self):
        auctions_table = AuctionsTable().read_table()

        last_index = max(auctions_table, key= itemgetter("auction_index"))["auction_index"]
        return last_index

    def set_index(self):
        return self.get_last_index() + 1

    def get_current_date(self):
        current_date = datetime.now(ZoneInfo("Asia/Macau"))
        return current_date.strftime("%d/%m/%Y %H:%M")
