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
        self.bid.add_argument("--preço", type= float)
        self.bid.add_argument("--pagamento")

        self.see = self.subparser.add_parser("ver")

        self.search = self.subparser.add_parser("buscar")
        self.search_subparser = self.search.add_subparsers(dest='criterion')

        self.search_winner = self.search_subparser.add_parser("arrematante")
        self.search_winner.add_argument("winner")

        self.search_product = self.search_subparser.add_parser("produto")
        self.search_product.add_argument("product")

        self.edit = self.subparser.add_parser("editar")
        self.edit.add_argument("winner")

        self.delete = self.subparser.add_parser("apagar")
        self.delete.add_argument("winner")

        self.total_sum = self.subparser.add_parser("dinheiros")

        self.subparser.add_parser("finalizar")

        self.args = self.argument_parser.parse_args()

    def create_auction(self):
        current_auction = self.dao_auction.get_active_auction()
        if not current_auction:
            new_auction = Auction(self.args.nome)
            self.dao_history_auctions.save_auction(new_auction)
            print(f'Leilão "{new_auction.name}" está criado e ativo no momento'.upper())
        else:
            print(f'Não é possível abrir um novo leilão enquanto o leilao "{current_auction.get("name")}" estiver'
                  f' ativo. Primeiro você deve finalizá-lo.'.upper())

    def add_new_bid(self):
        auction = self.dao_auction.get_active_auction()

        if auction and auction.get("status"):
            new_bid = Bid(auction.get("auction_index"),self.args.arrematante,
                          self.args.produto, self.args.preço, self.args.pagamento)

            self.dao_auction.save_bid(new_bid)
        else:
            print("Primeiro tem que criar um leilao, parceiro.".upper())

    def see_bids(self):
        bids_list = self.dao_auction.return_auction_bids()
        current_auction = self.dao_auction.get_active_auction()

        if current_auction:
            if not bids_list:
                print(f'Não há arremates ainda relacionados a este leilao "{current_auction.get("name")}".'.upper())
            else:
                for bid in bids_list:
                    print(f"{bid.get("bid_date")} -- {bid.get("winner")} -- {bid.get("product")}"
                          f" -- {bid.get("price")} -- {bid.get("payment")}\n")
        else:
            print("Quer ver arremates? tem que abrir um leilao, fera. No momento nao há leilao ativo.".upper())

    def custom_search(self):
        if self.args.criterion == "arrematante":
            self.search_bid_by_winner()

        elif self.args.criterion == "produto":
            self.search_bid_by_product()

    def search_bid_by_winner(self):
        bid_list = self.dao_auction.search_for_winner(self.args.winner)
        current_auction = self.dao_auction.get_active_auction()

        if current_auction:
            if bid_list:
                for bid in bid_list:
                    print(f"{bid.get("bid_date")} {bid.get("product")} {bid.get("winner")} "
                          f"{bid.get("price")} {bid.get("payment")}")
            else:
                print(f'Não há este arrematante "{self.args.winner}"')
        else:
            print("Não há leilao aberto. É impossivel ver arremates fora dum leilao")

    def search_bid_by_product(self):
        current_auction = self.dao_auction.get_active_auction()
        bid_list = self.dao_auction.search_for_product(self.args.product)

        if current_auction:
            if bid_list:
                for bid in bid_list:
                    print(f"{bid.get("bid_date")} {bid.get("product")} {bid.get("winner")} "
                          f"{bid.get("price")} {bid.get("payment")}")
            else:
                print(f'Não há este produto "{self.args.product}"')
        else:
            print("Não há leilao aberto. É impossivel ver arremates fora dum leilao")

    def edit_bid(self):
        current_auction = self.dao_auction.get_active_auction()

        if current_auction:
            bid_list = self.dao_auction.search_for_winner(self.args.winner)
            bid = bid_list[0]

            for index, bid in enumerate(bid_list):
                print(f"{index}º) - {bid.get("bid_date")} -- {bid.get("winner")} -- "
                  f"{bid.get("product")} -- {bid.get("price")} -- "
                  f"{bid.get("payment")}")

            if len(bid_list) > 1:
                position_bid = int(input("\nDigite a posição do arremate a ser editado: "))
                bid = self._return_a_dictionary(position_bid, bid_list)

            print(f"\nSerá editado o arremate: {bid.get("bid_date")} -- {bid.get("winner")} -- "
                  f"{bid.get("product")} -- {bid.get("price")} -- "
                  f"{bid.get("payment")}\n")

            new_winner = input("Nome do arrematante: ")
            new_product = input("Nome do produto: ")
            new_price = float(input("preço: "))
            new_payment = input("Digite 'True' para pago/ 'False' para nao pago: ")


            self.dao_auction.update_bid(bid, new_winner, new_product,
                                        new_price, new_payment)

            print("\n O Arremate foi editado.")
        else:
            print("Operação impossível")

    def delete_bid(self):
        current_auction = self.dao_auction.get_active_auction()

        if current_auction:
            bid_winner_list = self.dao_auction.search_for_winner(self.args.winner)
            if bid_winner_list:
                bid = bid_winner_list[0]

                for index, bid in enumerate(bid_winner_list):
                    print(f"\n{index}: {bid.get("bid_date")} -- {bid.get("winner")} -- {bid.get("product")} "
                          f"-- {bid.get("price")} -- {bid.get("payment")}")

                if len(bid_winner_list) > 1:
                    position = int(input("\nDigite a posição do arremate a ser excluido: "))
                    bid = self._return_a_dictionary(position, bid_winner_list)

                self.dao_auction.remove_bid(bid)
                print("\n Foi excluido o seguinte arremate:")
                print(f"{bid.get("bid_date")} -- {bid.get("winner")} -- {bid.get("product")} "
                          f"-- {bid.get("price")} -- {bid.get("payment")}")

            else:
                print("Ainda não há arremates salvos.")
        else:
            print("É preciso antes entrar num leilão.")

    def see_total_sum(self):
        current_auction = self.dao_auction.get_active_auction()

        if current_auction:
            total_sum = self.dao_auction.sum_bid_values()
            print(f"Até agora a receita total deste leilao tem sido R$ {total_sum}")
        else:
            print("Só é possível realizar esta operação num leilao ativo.")
    def end_auction(self):
        current_auction = self.dao_auction.get_active_auction()

        if current_auction and current_auction.get("status") == True:
            self.dao_auction.change_status_to_false(current_auction)
            print("leilao encerrado.".upper())
        else:
            print(f'Não há o que finalizar. Não há leilao ativo no momento.'.upper())

    def _return_a_dictionary(self, index: int, dict_list: list) -> dict:
        for position, item in enumerate(dict_list) :
            if index == position:
                return item
        return None


