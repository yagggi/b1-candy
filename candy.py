from decouple import config
from bigone.client import Client
from time import sleep


api_key = config('API_KEY')
client = Client(api_key)


class Candy:

    def __init__(self):
        self.client = client

    def check_uip_bitcny_order_book(self):
        pass

    def check_eth_bitcny_order_book(self):
        pass

    def place_bitcny_uip_order(self, qty, times):
        pass

    def place_uip_bitcny_order(self, qty, times):
        pass

    def revert_order(self):
        pass

    def check_order_list(self):
        pass

    def check_account(self):
        pass

    def get_uip_amount(self):
        pass

    def get_candy_amount(self):
        pass

    def get_bitcny_amount(self):
        pass

    def get_eth_amount(self):
        pass


if __name__ == '__main__':
    try:
        c = Candy()
        bitcny, candy, uip, eth = c.get_bitcny_amount(), c.get_candy_amount(), c.get_uip_amount(), c.get_eth_amount()
        print('BITCNY: {}, CANDY: {}, UIP: {}, ETH: {}'.format(bitcny, candy, uip, eth))
        c.place_bitcny_uip_order(4, 20)
        while True:
            pending_orders = c.check_order_list()
            if not pending_orders:
                break
            sleep(3)
            break
        bitcny, candy, uip, eth = c.get_bitcny_amount(), c.get_candy_amount(), c.get_uip_amount(), c.get_eth_amount()
        print('BITCNY: {}, CANDY: {}, UIP: {}, ETH: {}'.format(bitcny, candy, uip, eth))
    except Exception as e:
        print(e)