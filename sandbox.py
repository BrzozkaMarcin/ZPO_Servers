from servers import *

product1 = Product('a23',4.5)
product2 = Product('b43',1.5)


products = [Product('1Pa1ka1134', 1.1), Product('PP234', 2.8), Product('PP235', 14),Product('P42', 65),Product('Pw12', 1),Product('Pas1244', 1),Product('Pk12', 1)]

listserver = ListServer(products)
entries = listserver.get_entries(4)
for entry in entries:
    print(entry.name, entry.price)

mapserver = MapServer(products)
entries2 = mapserver.get_entries(4)
for entry in entries2:
    print(entry.name, entry.price)
