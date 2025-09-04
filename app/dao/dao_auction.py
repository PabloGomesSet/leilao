from leilao.base.databases.json.auctions_table import AuctionsTable
from leilao.base.databases.json.bid_table import BidTable
from leilao.base.models.bid import Bid


class DaoAuction:
    def __init__(self):
        self.bid_table = BidTable()
        self.auctions_table = AuctionsTable()

    def get_active_auction(self):
        auctions_list = self.auctions_table.read_table()

        for auction in auctions_list:
            if auction.get("status"):
                return auction
        return []

    def change_status_to_false(self, auction: dict):
        auctions_list = self.auctions_table.read_table()

        for item in auctions_list:
            if item.get("auction_index") == auction.get("auction_index"):
                item.update({"status": False})

        self.auctions_table.write_in_table(auctions_list)

    def save_bid(self, bid: Bid):
        dict_list = self.bid_table.read_table()
        dict_list.append(bid.convert_to_dictionary())

        self.bid_table.write_in_table(dict_list)
        print("Arremate salvo.".upper())

    def convert_dict_to_bid(self):
        dict_list = self.bid_table.read_table()
        current_auction = self.get_active_auction()
        bids_list = []

        if current_auction:
            for dictionary in dict_list:
                if current_auction.get("auction_index") == dictionary.get("auction_key"):
                    bids_list.append(dictionary)

        return bids_list



