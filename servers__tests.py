#!/usr/bin/python
# -*- coding: utf-8 -*-

# Marcin Brzózka, nr 405499
# Stanisław Dudiak, nr 406903
# Adam Pękala, nr 405380

import unittest
from collections import Counter

from servers import ListServer, Product, Client, MapServer, TooManyProductsFoundError

server_types = (ListServer, MapServer)

# Test dodatkowy sprawdzający rzucanie wyjątku ValueError dla produktu
class ProductTest(unittest.TestCase):
    def test_proper_name(self):
        # only_letters
        with self.assertRaises(ValueError):
            Product('ss', 2.0)

        # reverse
        with self.assertRaises(ValueError):
            Product('23ss', 2.0)

        # mixed
        with self.assertRaises(ValueError):
            Product("2S3f", 6.4)

        # only_numbers
        with self.assertRaises(ValueError):
            Product('23', 2.0)


class ServerTest(unittest.TestCase):
    def test_get_entries_returns_proper_entries(self):
        products = [Product('P12', 1), Product('PP234', 2), Product('PP235', 1)]
        for server_type in server_types:
            server = server_type(products)
            entries = server.get_entries(2)
            self.assertEqual(Counter([products[2], products[1]]), Counter(entries))

    def test_sort(self):
        products = [Product('XD123', 1), Product('ow121', 0.5), Product('PO235', 12), Product('wp131', 6), Product('w131', 99)]
        for server_type in server_types:
            server = server_type(products)
            entries = server.get_entries(2)
            lst1 = []
            lst2 = ['ow121', 'XD123', 'wp131', 'PO235']
            for i in range(len(entries)):
                lst1.append(entries[i].name)
            self.assertEqual(lst1, lst2)

    def test_TooManyProductsFoundError(self):
        products = [Product('X123', 3.5), Product('o121', 1), Product('P235', 1.5), Product('w131', 1),
                    Product('W32', 2), Product('x12', 2)]
        for server_type in server_types:
            server = server_type(products)
            with self.assertRaises(TooManyProductsFoundError):
                server.get_entries(1)


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
