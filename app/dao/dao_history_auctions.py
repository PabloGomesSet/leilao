from leilao.base.databases.json.auctions_table import AuctionsTable
from leilao.base.models.auction import Auction


class DaoHistoryAuctions:
    def __init__(self):
        self.auctions_table = AuctionsTable()

    def save_auction(self, auction: Auction):
        auctions_list = self.auctions_table.read_table()
        auctions_list.append(auction.convert_to_dictionary())

        self.auctions_table.write_in_table(auctions_list)

    def see_auctions(self):
        pass

    def search_for_an_auction(self):
        pass

    def see_total_revenue(self):
        pass