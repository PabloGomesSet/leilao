from argparse import ArgumentParser

from leilao.interfaces.cli.auction_cli import AuctionCli
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
    arg_parser.add_argument("option", choices=["leilao", "historico"])

    known_arg, unknown_arg = arg_parser.parse_known_args()

    if known_arg.option == "leilao":
        if unknown_arg:
            auction_cli = AuctionCli(unknown_arg)
            load_auction_menu(auction_cli)
        else:
            print('Junto com "leilao" é necessário informar a açao a ser realizada: novo, editar, ver...\n')

    elif known_arg.option == "historico":
        print("Ainda por fazer\n")

if __name__ == "__main__":
    main()