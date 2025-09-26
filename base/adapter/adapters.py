from datetime import datetime
from leilao.base.models.auction import Auction
from leilao.base.models.bid import Bid


def convert_bid_to_dictionary(bid: Bid):
    return {"bid_index": bid.bid_index,
            "bid_date": bid.bid_date,
            "winner": bid.winner,
            "product": bid.product,
            "price": bid.price,
            "payment": bid.payment,
            "auction_key": bid.auction_key}


def convert_dict_to_bid(dictionary: dict):
    bid = Bid(dictionary.get("auction_key"), dictionary.get("winner"), dictionary.get("product"),
              dictionary.get("price"), dictionary.get("payment"))
    bid.bid_index = dictionary.get("bid_index")
    bid.bid_date = dictionary.get("bid_date")

    return bid

def convert_to_auctions(dictionary: dict):
    auction = Auction(dictionary.get("name"))
    auction.auction_index = dictionary.get("auction_index")
    auction.status = dictionary.get("status")
    auction.auction_date = (datetime.strptime(dictionary.get("auction_date"), "%d/%m/%Y %H:%M")
                            .strftime("%d/%m/%Y %H:%M"))
    return auction

def convert_auction_to_dictionary(auction: Auction):
    return {"auction_index":auction.auction_index,
            "auction_date": auction.auction_date,
            "name":auction.name,
            "status": auction.status}