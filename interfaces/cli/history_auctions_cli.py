from argparse import ArgumentParser
from leilao.app.dao.dao_history_auctions import DaoHistoryAuctions


class HistoryAuctionCli:
    def __init__(self, argument):
        self.dao_history_auctions = DaoHistoryAuctions()

        argument_parser = ArgumentParser()
        self.subparser = argument_parser.add_subparsers(dest= "command")

        self.see_auction = self.subparser.add_parser("ver")

        self.search_auction = self.subparser.add_parser("buscar")
        self.search_auction.add_argument("nome")

        self.show_bids = self.subparser.add_parser("arremates")
        self.show_bids.add_argument("data")
        self.show_bids.add_argument("nome")

        self.args = argument_parser.parse_args(argument)
        #print("valor do command: ", self.args)


    def show_auctions(self):
        auctions_list = self.dao_history_auctions.list_auctions()

        for index, auction in enumerate(auctions_list):
            print(f'{index + 1}º) {auction.auction_date} -- {auction.name}')
            print("_________________________________________\n")

    def custom_search(self):
        auction = self.dao_history_auctions.search_for_an_auction(self.args.nome)

        if auction:
            print("_________________________________________\n")
            print(f' {auction.auction_date} -- {auction.name}')
            print("_________________________________________\n")
        else:
            print(f"Não há um leilao com este nome {self.args.nome}.")


    def show_bids_auction(self):
        auction = self.dao_history_auctions.return_an_auction(self.args.data, self.args.nome)

        print(f'\t\t\t Arremates de "{self.args.nome}"\n')
        if auction:
            bid_list = self.dao_history_auctions.list_bids(auction)
            for bid in bid_list:
                print(f'{bid.bid_date} -- {bid.product} -- {bid.winner}'
                            f' -- {bid.price} -- {bid.payment}')
                print("_________________________________________\n")
        else:
            print("Opa! Este leilao nao existe.")

