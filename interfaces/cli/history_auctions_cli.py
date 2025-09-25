from argparse import ArgumentParser
from leilao.app.dao.dao_history_auctions import DaoHistoryAuctions


class HistoryAuctionCli:
    def __init__(self, argument):
        self.dao_history_auctions = DaoHistoryAuctions()

        argument_parser = ArgumentParser()
        self.subparser = argument_parser.add_subparsers(dest= "command", help= '1- "ver" para visualizar toda a lista '
                                                                               'de leilões ja realizados\n2- "arremates" '
                                                                               'para ver os arremates de um determnado '
                                                                               'leilao\n 3- "remover" para apagar um leilao '
                                                                               'e os seus arremates\n 4- "editar" para mudar '
                                                                               'o nome de um leilao')

        self.see_auction = self.subparser.add_parser("ver")

        self.search_auction = self.subparser.add_parser("buscar")
        self.search_auction.add_argument("nome")

        self.show_bids = self.subparser.add_parser("arremates")
        self.show_bids.add_argument("data")
        self.show_bids.add_argument("nome")

        self.remove = self.subparser.add_parser("remover")
        self.remove.add_argument("data")
        self.remove.add_argument("nome")

        self.edit_name = self.subparser.add_parser("editar")
        self.edit_name.add_argument("data")
        self.edit_name.add_argument("nome")

        self.revenue = self.subparser.add_parser("dinheiros")
        self.revenue.add_argument("data")
        self.revenue.add_argument("nome")


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

        if auction and not auction.status:
            bid_list = self.dao_history_auctions.list_bids(auction)
            print(f'\t\t\t Arremates de "{self.args.nome}"\n')

            for bid in bid_list:
                print(f'{bid.bid_date} -- {bid.product} -- {bid.winner}'
                            f' -- {bid.price} -- {bid.payment}')
                print("_____________________________________________\n")
        else:
            print("\nOpa! Este leilao nao existe.")

    def remove_auction(self):
        auction = self.dao_history_auctions.return_an_auction(self.args.data, self.args.nome)

        if auction and not auction.status:
            self.dao_history_auctions.delete_bids(auction)
            self.dao_history_auctions.delete_auction(auction)
            print(f'Leilão {auction.name} removido completamente.')
        else:
            print("Leilão não encontrado.")

    def edit_auction(self):
        auction = self.dao_history_auctions.return_an_auction(self.args.data, self.args.nome)

        if auction and not auction.status:
            self.dao_history_auctions.modify_auction(auction)
        else:
            print("Leilão nao encontrado.")

    def see_total_revenue(self):
        auction = self.dao_history_auctions.return_an_auction(self.args.data, self.args.nome)

        if auction and not auction.status:
            revenue = self.dao_history_auctions.see_revenue(auction)

            print(f"O Valor total arrecadado neste leilão foi R$ {revenue}")
        else:
            print("Leilão nao encontrado.")
