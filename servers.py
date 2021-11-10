#!/usr/bin/python
# -*- coding: utf-8 -*-

# from _typeshed import Self
from typing import List, Optional
from abc import ABC, abstractmethod


class Product:
    # FIXME: klasa powinna posiadać metodę inicjalizacyjną przyjmującą argumenty wyrażające nazwę produktu (typu str)
    #  i jego cenę (typu float) -- w takiej kolejności -- i ustawiającą atrybuty `name` (typu str) oraz `price` (typu
    #  float)

    def __init__(self, name: str, price: float):
        self.name: str = name
        self.price: float = price

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, new):
        ind = 0
        for x, y in enumerate(new):
            try:
                int(y)
            except ValueError:
                pass
            else:
                ind = x
                break
        if not (new[0:ind].isalpha() and new[ind:].isdigit()):
            raise ValueError
        else:
            self._name = new

    def __eq__(self, other):
        return isinstance(other, Product) and self.name == other.name and self.price == other.price

    def __hash__(self):
        return hash((self.name, self.price))


class TooManyProductsFoundError(Exception):
    # Reprezentuje wyjątek związany ze znalezieniem zbyt dużej liczby produktów.
    def __init__(self, n_returned_entries, n_max_returned_entries):
        super().__init__(self)
        self.n_returned_entries = n_returned_entries
        self.n_max_returned_entries = n_max_returned_entries
        print('number of entries exceeded by:', self.n_returned_entries - self.n_max_returned_entries)


# FIXME: Każada z poniższych klas serwerów powinna posiadać: (1) metodę inicjalizacyjną przyjmującą listę obiektów
#  typu `Product` i ustawiającą atrybut `products` zgodnie z typem reprezentacji produktów na danym serwerze,
#  (2) możliwość odwołania się do atrybutu klasowego `n_max_returned_entries` (typu int) wyrażający maksymalną
#  dopuszczalną liczbę wyników wyszukiwania, (3) możliwość odwołania się do metody `get_entries(self, n_letters)`
#  zwracającą listę produktów spełniających kryterium wyszukiwania

class Server(ABC):
    def __init__(self) -> None:
        super().__init__()

    n_max_returned_entries = 5
    products = None

    def get_entries(self, n_letters: int = 1) -> List[Product]:
        products = self.get_all_products()
        product_list = []
        ascii_letters = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
        digits = '0123456789'
        for product in products:
            n_chars = product.name[0:n_letters]
            nums2 = product.name[n_letters:n_letters + 2]
            nums3 = product.name[n_letters:n_letters + 3]
            if all(item in ascii_letters for item in n_chars):
                if all(item in digits for item in nums2) or all(item in digits for item in nums3):
                    product_list.append(product)
            if len(product_list) > self.n_max_returned_entries:
                raise TooManyProductsFoundError(len(product_list), self.n_max_returned_entries)
        product_list.sort(key=lambda x: x.price)
        return product_list

    @abstractmethod
    def get_all_products(self):
        pass


class ListServer(Server):
    def __init__(self, products) -> None:
        super().__init__()

        self.products = products

    def get_all_products(self):
        return self.products


class MapServer(Server):

    def __init__(self, products) -> None:
        super().__init__()
        self.products = {}
        for product in products:
            self.products[product.name] = product

    def get_all_products(self):
        product_list = []
        for key in self.products.keys():
            product_list.append(self.products[key])
        return product_list


class Client:
    # FIXME: klasa powinna posiadać metodę inicjalizacyjną przyjmującą obiekt reprezentujący serwer

    def __init__(self, server_: Server) -> None:
        self.server = server_

    def get_total_price(self, n_letters: Optional[int]) -> Optional[float]:
        try:
            sum_price = 0
            lst_product = self.server.get_entries(n_letters)

            if not lst_product:
                return None

            for i in range(len(lst_product)):
                sum_price += lst_product[i].price

        except TooManyProductsFoundError:
            return None
        return sum_price
