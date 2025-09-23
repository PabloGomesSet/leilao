from datetime import datetime
from leilao.app.dao.dao_auction import DaoAuction
from leilao.base.databases.json.auctions_table import AuctionsTable
from leilao.base.databases.json.bid_table import BidTable
from leilao.base.models.auction import Auction
from leilao.base.models.bid import Bid


class DaoHistoryAuctions:
    def __init__(self):
        self.auctions_table = AuctionsTable()
        self.bid_table = BidTable()
        self.dao_auction = DaoAuction()

    def save_auction(self, auction: Auction):
        auctions_list = self.auctions_table.read_table()
        auctions_list.append(self._convert_to_dictionary(auction))

        self.auctions_table.write_in_table(auctions_list)

    def list_auctions(self) -> list[Auction]:
        dict_list = self.auctions_table.read_table()
        auctions_list = list()

        for item in dict_list[1:]:
            if not item.get("status"):
                auctions_list.append(self._convert_to_auctions(item))
        return auctions_list

    def search_for_an_auction(self, auction_name):
        auctions_list = self.auctions_table.read_table()

        for item in auctions_list:
            if not item.get("status") and item.get("name") == auction_name:
                auction = self._convert_to_auctions(item)
                return auction
        return False

    def list_bids(self, auction: Auction)-> list[Bid]:
        list_bid_dict = BidTable().read_table()
        list_bid_object = list()

        for item in list_bid_dict:
            new_bid = self.dao_auction.convert_dict_to_bid(item)
            if auction.auction_index == new_bid.auction_key:
                list_bid_object.append(new_bid)
        return list_bid_object

    def delete_auction(self, auction: Auction):
        auction_list = self.auctions_table.read_table()
        dictionary = self._convert_to_dictionary(auction)

        for item in auction_list:
            if not item.get("status") and item.get("auction_index") == dictionary.get("auction_index"):
                auction_list.remove(item)
                self.auctions_table.write_in_table(auction_list)
                return True
        return False

    def delete_bids(self, auction: Auction):
        bids_list = self.bid_table.read_table()
        dictionary = self._convert_to_dictionary(auction)

        for item in bids_list:
            if not item.get("status") and item.get("auction_key") == dictionary.get("auction_index"):
                bids_list.remove(item)
                self.bid_table.write_in_table(bids_list)


    def _convert_to_dictionary(self, auction: Auction):
        return {"auction_index":auction.auction_index,
                "auction_date": auction.auction_date,
                "name":auction.name,
                "status": auction.status}

    def _convert_to_auctions(self, dictionary: dict):
        auction = Auction(dictionary.get("name"))
        auction.auction_index = dictionary.get("auction_index")
        auction.auction_date = (datetime.strptime(dictionary.get("auction_date"), "%d/%m/%Y %H:%M")
                                .strftime("%d/%m/%Y %H:%M"))
        return auction

    def return_an_auction(self, date, name):
        auction_list = self.auctions_table.read_table()

        for item in auction_list:
            if item.get("auction_date") == date and item.get("name") == name:
                return self._convert_to_auctions(item)
        return False