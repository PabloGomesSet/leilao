from argparse import ArgumentParser

from leilao.app.dao.dao_auction import DaoAuction
from leilao.app.dao.dao_history_auctions import DaoHistoryAuctions
from leilao.base.models.auction import Auction
from leilao.base.models.bid import Bid


class AuctionCli:
    def __init__(self):
        self.dao_auction = DaoAuction()
        self.dao_history_auctions = DaoHistoryAuctions()

        self.argument_parser = ArgumentParser()
        self.subparser = self.argument_parser.add_subparsers(dest="command")

        self.auction_name  = self.subparser.add_parser("leilao")
        self.auction_name.add_argument("--nome")

        self.bid = self.subparser.add_parser("arremate")
        self.bid.add_argument("--arrematante")
        self.bid.add_argument("--produto")
        self.bid.add_argument("--preço")
        self.bid.add_argument("--pagamento")

        self.subparser.add_parser("finalizar")

        self.args = self.argument_parser.parse_args()


    def create_auction(self):
        new_auction = Auction(self.args.nome)
        self.dao_history_auctions.save_auction(new_auction)
        print(f'Leilão "{new_auction.name}" está criado e ativo no momento'.upper())


    def add_new_bid(self):
        auction = self.dao_auction.get_active_auction()

        if auction and auction.get("status"):
            new_bid = Bid(auction.get("auction_index"),self.args.arrematante,
                          self.args.produto, self.args.preço, self.args.pagamento)

            self.dao_auction.save_bid(new_bid)
        else:
            print("Primeiro tem que criar um leilao, parceiro.".upper())

    def end_auction(self):
        current_auction = self.dao_auction.get_active_auction()

        if current_auction and current_auction.get("status") == True:
            self.dao_auction.change_status_to_false(current_auction)
            print("leilao encerrado.".upper())
        else:
            print(f'Não há leilao ativo no momento'.upper())
