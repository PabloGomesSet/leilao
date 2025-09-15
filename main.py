from leilao.interfaces.cli.auction_cli import AuctionCli
"""
Pendencias:
1- Na função editar da cli, fazer a validação da situação em que nao há arremates salvos.
"""

def main():
    auction_cli = AuctionCli()

    if auction_cli.args.command == "leilao":
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

if __name__ == "__main__":
    main()