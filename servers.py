#!/usr/bin/python
# -*- coding: utf-8 -*-

# from _typeshed import Self
from typing import List, Optional
from abc import ABC, abstractmethod


class Product:
    # FIXME: klasa powinna posiadać metodę inicjalizacyjną przyjmującą argumenty wyrażające nazwę produktu (typu str)
    #  i jego cenę (typu float) -- w takiej kolejności -- i ustawiającą atrybuty `name` (typu str) oraz `price` (typu
    #  float)

    def __eq__(self, other):
        return None  # FIXME: zwróć odpowiednią wartość

    def __hash__(self):
        return hash((self.name, self.price))


class TooManyProductsFoundError:
    # Reprezentuje wyjątek związany ze znalezieniem zbyt dużej liczby produktów.
    pass


# FIXME: Każada z poniższych klas serwerów powinna posiadać: (1) metodę inicjalizacyjną przyjmującą listę obiektów
#  typu `Product` i ustawiającą atrybut `products` zgodnie z typem reprezentacji produktów na danym serwerze,
#  (2) możliwość odwołania się do atrybutu klasowego `n_max_returned_entries` (typu int) wyrażający maksymalną
#  dopuszczalną liczbę wyników wyszukiwania, (3) możliwość odwołania się do metody `get_entries(self, n_letters)`
#  zwracającą listę produktów spełniających kryterium wyszukiwania

class Server(ABC):
    def __init__(self) -> None:
        self.products = 0
        super().__init__()
    n_max_returned_entries = 10
    
    def get_entries(self,n_letters:int = 1) -> List[Product]:
        products = self.get_all_products(self.products)
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
                print('too many entries')
                return 0 
            product_list = sorted(product_list,key = product.price)
        return product_list

    @abstractmethod
    def get_all_products(self):
        pass


class ListServer(Server):
    def __init__(self,products) -> None:
        super().__init__(self)

        self.products = products

    def get_all_products(self):
        return self.products

class MapServer(Server):

    def __init__(self,products) -> None:
        super().__init__(self)
        self.products = {}
        for product in products:
            self.products[product.name] = product

    def get_all_products(self):
        product_list = []
        for product in self.products:
            product_list.append(product)
        return product_list


class Client:
    # FIXME: klasa powinna posiadać metodę inicjalizacyjną przyjmującą obiekt reprezentujący serwer

    def get_total_price(self, n_letters: Optional[int]) -> Optional[float]:
        raise NotImplementedError()
