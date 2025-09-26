
from datetime import datetime
from operator import itemgetter
from zoneinfo import ZoneInfo
from leilao.base.databases.json.bid_table import BidTable
from leilao.base.models.product import Product

class Bid:
    def __init__(self, auction_key, winner, product:Product, price:float, payment: bool):
        self.bid_index = self.set_index()
        self.auction_key = auction_key
        self.bid_date = self.get_current_date()
        self.winner = winner
        self.product = product
        self.price = price
        self.payment = payment

    def get_last_index(self):
        bid_table = BidTable().read_table()

        last_index = max(bid_table, key= itemgetter("bid_index"))["bid_index"]
        return last_index

    def set_index(self) -> int:
        return self.get_last_index() + 1

    def get_current_date(self):
        bid_date = datetime.now(ZoneInfo("America/Sao_Paulo"))

        return bid_date.strftime("%d/%m/%y %H:%M")