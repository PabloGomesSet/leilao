from operator import itemgetter
from leilao.base.databases.json.bid_table import BidTable
from leilao.base.models.product import Product


class Bid:
    def __init__(self, auction_key, auction_date, winner, product:Product, price:float, payment: bool):
        self.bid_index = self.set_index()
        self.auction_key = auction_key
        self.auction_date = auction_date
        self.winner = winner
        self.product = product
        self.price = price
        self.payment = payment

    def convert_to_dictionary(self):
        return {"bid_index": self.bid_index,
                "auction_key": self.auction_key,
                "auction_date": self.auction_date,
                "winner": self.winner,
                "product": self.product,
                "price":self.price,
                "payment": self.payment}

    def get_last_index(self):
        bid_table = BidTable().read_table()

        last_index = max(bid_table, key= itemgetter("bid_index"))["bid_index"]
        return last_index

    def set_index(self) -> int:
        return self.get_last_index() + 1