from datetime import datetime


class AuctionHistory:
    def __init__(self, auction_key: int, auction_date: datetime):
        self.index = self.get_last_index()
        self.auction_key = auction_key
        self.auction_date = auction_date


    def get_last_index(self):
        return 0