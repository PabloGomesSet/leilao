from argparse import ArgumentParser

from leilao.interfaces.cli.auction_cli import AuctionCli
from leilao.interfaces.cli.history_auctions_cli import HistoryAuctionCli

"""
Pendencias:
1- Na função editar da cli, fazer a validação da situação em que nao há arremates salvos.
"""

def load_auction_menu(auction_cli):
    if auction_cli.args.command == "novo":
        auction_cli.create_auction()
    elif auction_cli.args.command == "arremate":
        auction_cli.add_new_bid()
    elif auction_cli.args.command == "finalizar":
        auction_cli.end_auction()
    elif auction_cli.args.command == "ver":
        auction_cli.see_bids()
    elif auction_cli.args.command == "buscar":
        auction_cli.custom_search()
    elif auction_cli.args.command == "editar":
        auction_cli.edit_bid()
    elif auction_cli.args.command == "apagar":
        auction_cli.delete_bid()
    elif auction_cli.args.command == "dinheiros":
        auction_cli.see_total_sum()
    elif auction_cli.args.command == "pagar":
        auction_cli.to_pay()

def main():
    arg_parser = ArgumentParser()
    arg_parser.add_argument("option", choices=["leilao", "historico"],
                            help= 'Pra começar voce tem que decidir se quer iniciar um novo leilão (digitando '
                                  'leilao mais a acao a ser realizada: "leilao novo primeiro leilao" ou se quer '
                                  'ver o historico de leilões: "histórico ver".')

    known_arg, unknown_arg = arg_parser.parse_known_args()

    if known_arg.option == "leilao":
        if unknown_arg:
            auction_cli = AuctionCli(unknown_arg)
            load_auction_menu(auction_cli)
        else:
            print('Junto com "leilao" é necessário informar a açao a ser realizada: novo, editar, ver...\n')

    elif known_arg.option == "historico":
        history_auctions_cli = HistoryAuctionCli(unknown_arg)

        if history_auctions_cli.args.command == "ver":
            history_auctions_cli.show_auctions()
        elif history_auctions_cli.args.command == "buscar":
            history_auctions_cli.custom_search()
        elif history_auctions_cli.args.command == "arremates":
            history_auctions_cli.show_bids_auction()
        elif history_auctions_cli.args.command == "remover":
            history_auctions_cli.remove_auction()
        elif history_auctions_cli.args.command == "editar":
            history_auctions_cli.edit_auction()
        elif history_auctions_cli.args.command == "dinheiros":
            history_auctions_cli.see_total_revenue()

if __name__ == "__main__":
    main()