#!/usr/bin/python
# -*- coding: utf-8 -*-

import unittest
from collections import Counter

from servers import ListServer, Product, Client, MapServer

server_types = (ListServer, MapServer)

class ProductTest(unittest.TestCase):

    def test_proper_name(self):
        with self.assertRaises(ValueError):
            only_letters = Product('ss', 2.0)

        with self.assertRaises(ValueError):
            reverse = Product('23ss', 2.0)

        with self.assertRaises(ValueError):
            mixed = Product("2S3f", 6.4)

        with self.assertRaises(ValueError):
            only_numbers = Product('23', 2.0)


class ServerTest(unittest.TestCase):

    def test_get_entries_returns_proper_entries(self):
        products = [Product('P12', 1), Product('PP234', 2), Product('PP235', 1)]
        for server_type in server_types:
            server = server_type(products)
            entries = server.get_entries(2)
            self.assertEqual(Counter([products[2], products[1]]), Counter(entries))


class ClientTest(unittest.TestCase):
    def test_total_price_for_normal_execution(self):
        products = [Product('PP234', 2), Product('PP235', 3)]
        for server_type in server_types:
            server = server_type(products)
            client = Client(server)
            self.assertEqual(5, client.get_total_price(2))

    def test_total_price_for_abnormal_execution(self):
        products = [Product('X123', 3.5), Product('o121', 1), Product('P235', 1.5), Product('w131', 1),
                    Product('W32', 2), Product('x12', 2)]
        for server_type in server_types:
            server = server_type(products)
            client = Client(server)
            self.assertEqual(None, client.get_total_price(1))
            self.assertEqual(None, client.get_total_price(10))
if __name__ == '__main__':
    unittest.main()
