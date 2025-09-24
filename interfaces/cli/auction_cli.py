import argparse
from argparse import ArgumentParser
from datetime import datetime
from leilao.app.dao.dao_auction import DaoAuction
from leilao.app.dao.dao_history_auctions import DaoHistoryAuctions
from leilao.base.databases.json.bid_table import BidTable
from leilao.base.models.auction import Auction
from leilao.base.models.bid import Bid


class AuctionCli:
    def __init__(self, typed_argument: list):
        self.dao_auction = DaoAuction()
        self.dao_history_auctions = DaoHistoryAuctions()

        self.argument_parser = ArgumentParser()
        self.subparser = self.argument_parser.add_subparsers(dest="command")

        self.auction_name  = self.subparser.add_parser("novo")
        self.auction_name.add_argument("nome")

        self.bid = self.subparser.add_parser("arremate")
        self.bid.add_argument("arrematante")
        self.bid.add_argument("produto")
        self.bid.add_argument("preço", type= float)
        self.bid.add_argument("pagamento", type = self._get_payment_status)

        self.see = self.subparser.add_parser("ver")

        self.search = self.subparser.add_parser("buscar")
        self.search_subparser = self.search.add_subparsers(dest='criterion')

        self.search_winner = self.search_subparser.add_parser("arrematante")
        self.search_winner.add_argument("winner")

        self.search_product = self.search_subparser.add_parser("produto")
        self.search_product.add_argument("product")

        self.edit = self.subparser.add_parser("editar")
        self.edit.add_argument("data")
        self.edit.add_argument("arrematante")
        self.edit.add_argument("produto")
        self.edit.add_argument("preço", type = float)
        self.edit.add_argument("pagamento", type= self._get_payment_status)

        self.delete = self.subparser.add_parser("apagar")
        self.delete.add_argument("data")
        self.delete.add_argument("arrematante")
        self.delete.add_argument("produto")
        self.delete.add_argument("preço", type = float)
        self.delete.add_argument("pagamento", type= self._get_payment_status)

        self.total_sum = self.subparser.add_parser("dinheiros")

        self.pay = self.subparser.add_parser("pagar")
        self.pay.add_argument("data")
        self.pay.add_argument("arrematante")
        self.pay.add_argument("produto")
        self.pay.add_argument("preço", type= float)
        self.pay.add_argument("pagamento", type= self._get_payment_status)

        self.subparser.add_parser("finalizar")

        self.args = self.argument_parser.parse_args(typed_argument)
        print(self.args)

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
        current_auction = self.dao_auction.get_active_auction()
        auction = self.dao_history_auctions.convert_to_auctions(current_auction)
        bids_list = self.dao_auction.return_auction_bids(auction)

        if auction:
            if not bids_list:
                print(f'Não há arremates ainda relacionados a este leilao "{current_auction.get("name")}".'.upper())
            else:
                for bid in bids_list:
                    print(f"{bid.bid_date} -- {bid.winner} -- {bid.product}"
                          f" -- R$ {bid.price} -- {bid.payment}\n")
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
            bid_index = self._return_a_index(self.args.data, self.args.arrematante,
                                             self.args.produto, self.args.preço, self.args.pagamento)

            if bid_index:
                modified_dict = {"bid_index": bid_index, "bid_date":self.args.data, "winner": self.args.arrematante,
                                 "product": self.args.produto, "price": self.args.preço, "payment": self.args.pagamento,
                                 "auction_key":current_auction.get("auction_index")}

                print(f"\nSerá editado o arremate: {modified_dict.get("bid_date")} -- {modified_dict.get("winner")} "
                      f"-- {modified_dict.get("product")} -- {modified_dict.get("price")} -- "
                      f"{modified_dict.get("payment")}\n")

                new_winner = input("Nome do arrematante: ")
                new_product = input("Nome do produto: ")
                new_price = input("preço: ")
                value_payment = input("Digite 'True' para pago/ 'False' para nao pago: ")
                new_payment = self._get_payment_status(value_payment)

                self.dao_auction.modify_bid(modified_dict, new_winner, new_product,
                                            new_price, new_payment)
            else:
                print("\nArremate não encontrado")
        else:
            print("Não há leilão ativo. Operação impossível.")

    def delete_bid(self):
        current_auction = self.dao_auction.get_active_auction()

        if current_auction:
            index = self._return_a_index(self.args.data, self.args.arrematante, self.args.produto,
                                                    self.args.preço, self.args.pagamento)

            bid_for_deletion = {"bid_index": index, "bid_date":self.args.data, "winner": self.args.arrematante,
                             "product": self.args.produto, "price": self.args.preço, "payment": self.args.pagamento,
                             "auction_key":current_auction.get("auction_index")}

            msg_return = self.dao_auction.remove_bid(bid_for_deletion)
            if msg_return:
                print("\n Foi excluido o seguinte arremate:")
                print(f"{bid_for_deletion.get("bid_date")} -- {bid_for_deletion.get("winner")} -- "
                      f"{bid_for_deletion.get("product")} -- {bid_for_deletion.get("price")} -- "
                      f"{bid_for_deletion.get("payment")}")
            else:
                print("Arremate não encontrado.")
        else:
            print("É preciso antes entrar num leilão.")

    def see_total_sum(self):
        current_auction = self.dao_auction.get_active_auction()

        if current_auction:
            total_sum = self.dao_auction.sum_bid_values(current_auction.get("auction_index"))
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

    def _return_a_index(self, date: datetime, winner, product, price:float, payment:bool) -> int:
       bids = BidTable().read_table()
       list_values_bid = [date, winner, product, price, payment]
       current_auction = self.dao_auction.get_active_auction()

       for item in bids:
           l_item = list(item.values())
           if item.get("auction_key") == current_auction.get("auction_index"):
               if l_item[1:-1] == list_values_bid:
                   return item.get("bid_index")
       return False

    def _get_payment_status(self, true_or_false):
        if true_or_false.title() == "True":
            return True
        elif true_or_false.title() == "False":
            return False
        else:
            raise argparse.ArgumentTypeError('No campo "Pagamento", só vale digitar "True" ou "False".')

    def to_pay(self):
        current_auction = self.dao_auction.get_active_auction()

        if current_auction:
            index = self._return_a_index(self.args.data, self.args.arrematante, self.args.produto,
                                          self.args.preço, self.args.pagamento)
            if index:
                bid = {"bid_index": index, "bid_date":self.args.data, "winner": self.args.arrematante,
                       "product": self.args.produto, "price": self.args.preço, "payment": self.args.pagamento,
                       "auction_key":current_auction.get("auction_index")}

                return_msg = self.dao_auction.change_payment_status(bid)
                if return_msg:
                    print("\n Arremate marcado como pago.")
                else:
                    print('\n Desmarcado o campo "Pagamento".')
            else:
                print("Arremate não encontrado.")
        else:
            print("\n É preciso antes criar um novo leilão.")


