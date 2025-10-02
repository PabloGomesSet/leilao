from datetime import datetime
from zoneinfo import ZoneInfo
from leilao.base.adapter.adapters import convert_to_auctions, convert_dict_to_bid, convert_bid_to_dictionary
from leilao.base.databases.json.auctions_table import AuctionsTable
from leilao.base.databases.json.bid_table import BidTable
from leilao.base.databases.spreasheets.functions import update_spreadsheets
from leilao.base.models.auction import Auction
from leilao.base.models.bid import Bid


class DaoAuction:
    def __init__(self):
        self.bid_table = BidTable()
        self.auctions_table = AuctionsTable()

    def get_active_auction(self):
        dict_list = self.auctions_table.read_table()

        for item in dict_list:
            if item.get("status"):
                return convert_to_auctions(item)
        return False

    def change_status_to_false(self, auction: Auction):
        auctions_list = self.auctions_table.read_table()

        for item in auctions_list[1:]:
            item_obj = convert_to_auctions(item)
            if item_obj.auction_index == auction.auction_index:
                item.update({"status": False})

        self.auctions_table.write_in_table(auctions_list)

    def save_bid(self, bid: Bid):
        dict_list = self.bid_table.read_table()
        dict_list.append(convert_bid_to_dictionary(bid))

        self.bid_table.write_in_table(dict_list)
        update_spreadsheets(dict_list)

        print("Arremate salvo.".upper())

    def return_auction_bids(self, auction: Auction):
        dict_list = self.bid_table.read_table()
        bids_list = []

        if auction:
            for item in dict_list:
                bid = convert_dict_to_bid(item)
                if auction.auction_index == bid.auction_key:
                    bids_list.append(bid)

        return bids_list

    def search_for_winner(self, winner):
        dict_list = self.bid_table.read_table()
        auction = self.get_active_auction()

        winner_list = []
        if auction:
            for item in dict_list:
                bid = convert_dict_to_bid(item)
                if bid.auction_key == auction.auction_index and bid.winner == winner:
                    winner_list.append(bid)
            return winner_list
        return False

    def search_for_product(self, product):
        dict_list, auction = self.bid_table.read_table(), self.get_active_auction()
        product_list = []
        
        if auction:
            for item in dict_list:
                bid = convert_dict_to_bid(item)
                if bid.auction_key == auction.auction_index and bid.product == product:
                    product_list.append(bid)
            return product_list
        return False

    def modify_bid(self, bid: dict, winner, product, price, payment):
        bid_list, validator = self.bid_table.read_table(), False

        for item in bid_list:
            if item == bid:
                item.update({"winner": winner, "product": product, "price": float(price),
                             "payment": payment, "bid_date": datetime.now(ZoneInfo("America/Sao_Paulo"))
                             .strftime("%d/%m/%Y %H:%M")})
                validator = True

        self.bid_table.write_in_table(bid_list)
        return validator

    def remove_bid(self, bid: dict):
        bid_list = self.bid_table.read_table()

        for item in bid_list:
            if item.get("bid_index") == bid.get("bid_index"):
                bid_list.remove(item)
                self.bid_table.write_in_table(bid_list)
                update_spreadsheets(bid_list)
                return True
        return False

    def sum_bid_values(self,auction: Auction) -> float:
        bid_list = self.bid_table.read_table()
        total_sum = 0.0

        for item in bid_list:
            bid = convert_dict_to_bid(item)
            if bid.auction_key == auction.auction_index:
                if bid.payment:
                    total_sum += float(bid.price)
        return total_sum

    def change_payment_status(self, b: Bid):
        bid_list = self.bid_table.read_table()
        current_auction = self.get_active_auction()

        for item in bid_list:
            bid_new = convert_dict_to_bid(item)
            if bid_new.auction_key == current_auction.auction_index:
                if bid_new.bid_index == b.bid_index:
                    if bid_new.payment:
                        item["payment"] = False
                        self.bid_table.write_in_table(bid_list)
                        return False
                    else:
                        item["payment"] = True
                        self.bid_table.write_in_table(bid_list)
                        return True
        return None

