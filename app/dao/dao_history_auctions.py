from leilao.base.databases.json.auctions_table import AuctionsTable
from leilao.base.models.auction import Auction


class DaoHistoryAuctions:
    def __init__(self):
        self.auctions_table = AuctionsTable()

    def save_auction(self, auction: Auction):
        auctions_list = self.auctions_table.read_table()
        auctions_list.append(self._convert_to_dictionary(auction))

        self.auctions_table.write_in_table(auctions_list)

    def list_auctions(self) -> list:
        dict_list = self.auctions_table.read_table()
        auctions_list = list()

        for item in dict_list:
            auctions_list.append(self._convert_to_auctions(item))

        return auctions_list

    def search_for_an_auction(self):
        pass

    def _convert_to_dictionary(self, auction: Auction):
        return {"auction_index":auction.auction_index,
                "auction_date":auction.auction_date,
                "name":auction.name,
                "status": auction.status}

    def _convert_to_auctions(self, dictionary: dict):
        auction = (dictionary.get("auction_index"), dictionary.get("auction_date"), dictionary.get("name"),
                   dictionary.get("status"))
        return auction