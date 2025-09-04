from argparse import ArgumentParser
from leilao.interfaces.cli.auction_cli import AuctionCli


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

def choice_options():
    argument_parser = ArgumentParser()
    argument_parser.add_argument("option", choices= ["novo", "historico"],
                                 help = "digite 'novo' para criar um novo leilão e 'historico' para "
                                 "ver todos os leiloes")

    args = argument_parser.parse_args()
    return args.option


if __name__ == "__main__":

    main()