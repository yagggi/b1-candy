#!/usr/bin/env python
from decouple import config
from bigone.client import Client
from time import sleep
from decimal import Decimal
import sys
import math

api_key = config('API_KEY')


class Candy:

    def __init__(self):
        self.client = Client(api_key)

    def get_uip_bnc_bid_price(self):
        market = self.client.get_market('UIP-BNC')
        bids = market.get('bids')
        if not bids:
            raise Exception('get uip-bnc bid price failed.')
        price = bids[0].get('price', '0')
        return price

    def get_uip_bnc_ask_price(self):
        market = self.client.get_market('UIP-BNC')
        asks = market.get('asks')
        if not asks:
            raise Exception('get uip-bnc ask price failed.')
        price = asks[0].get('price', '0')
        return price

    def place_uip_bnc_bid_order(self, qty, times, price=None):
        if not price:
            price = self.get_uip_bnc_bid_price()
        order_list = []
        for _ in range(times):
            trans = self.client.create_order('UIP-BNC', self.client.SIDE_BID, price, str(qty))
            order_list.append(trans['order_id'])
            sleep(1)
        return order_list

    def place_uip_bnc_ask_order(self, qty, times, price=None):
        if not price:
            price = self.get_uip_bnc_ask_price()
        order_list = []
        for _ in range(times):
            trans = self.client.create_order('UIP-BNC', self.client.SIDE_ASK, price, str(qty))
            order_list.append(trans['order_id'])
            sleep(1)
        return order_list

    def cancle_order(self, order_id):
        self.client.cancel_order(order_id)

    def check_orders(self, symbol):
        return self.client.get_orders(symbol)

    def check_accounts(self):
        res = self.client.get_accounts()
        accounts_dic = {}
        for x in res:
            accounts_dic[x['account_type']] = dict(x)
        self.accounts_dic = accounts_dic
        return self.accounts_dic

    def get_uip_amount(self):
        res = self.check_accounts().get('UIP')
        return Decimal(res.get('active_balance'))

    def get_candy_amount(self):
        res = self.check_accounts().get('CANDY')
        return Decimal(res.get('active_balance'))

    def get_bnc_amount(self):
        res = self.check_accounts().get('BNC')
        return Decimal(res.get('active_balance'))

    def get_eth_amount(self):
        res = self.check_accounts().get('ETH')
        return Decimal(res.get('active_balance'))


if __name__ == '__main__':
    try:
        c = Candy()
        bitcny, candy, uip, eth = c.get_bnc_amount(), c.get_candy_amount(), c.get_uip_amount(), c.get_eth_amount()
        print('BITCNY: {}, CANDY: {}, UIP: {}, ETH: {}'.format(bitcny, candy, uip, eth))

        if len(sys.argv) > 1:
            trades_times = int(sys.argv[1])
        else:
            trades_times = 20

        while True:
            bid_price = c.get_uip_bnc_bid_price()
            ask_price = c.get_uip_bnc_ask_price()
            print('UIP-BNC bid price: {}, ask price: {}'.format(bid_price, ask_price))

            if math.fabs(Decimal(bid_price) - Decimal(ask_price)) > 0.01:
                print('too much between ask and bid, waiting...')
                sleep(5)
                continue

            times = math.ceil(trades_times / 2)
            print(
                'preparing to place {0} bid orders with price{1} and {0} ask orders with price {2}'.format(
                    times, bid_price, ask_price
                )
            )
            ask_orders = c.place_uip_bnc_ask_order(4, times)
            bid_orders = c.place_uip_bnc_bid_order(4, times)
            break

        while True:
            pending_orders = c.check_orders('UIP-BNC')
            if not pending_orders:
                break
            print('pending orders: {}'.format(len(pending_orders)))
            sleep(3)
            continue
        bitcny, candy, uip, eth = c.get_bnc_amount(), c.get_candy_amount(), c.get_uip_amount(), c.get_eth_amount()
        print('BITCNY: {}, CANDY: {}, UIP: {}, ETH: {}'.format(bitcny, candy, uip, eth))
        print('SUCCESS')
    except Exception as e:
        print(e)