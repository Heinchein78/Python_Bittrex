import time

from bittrex import bittrex
from cursesmenu import *
from cursesmenu.items import *

my_bittrex = bittrex.Bittrex("b91292ec5202437599f1382ebf8dd77a", "b7ade1e83bd74313a3f3324c189aa97e")


def loop_open_order(market, marketbtc):
    open_order = my_bittrex.get_open_orders(marketbtc)['result']
    for i in range(len(open_order)):
        type_order = open_order[i]['OrderType']
        return str(type_order)


def pump():
    print("Bot_PUMP")
    balance_dispo = my_bittrex.get_balance("BTC")['result']['Balance']
    print("Voici la balance disponible: " + str(balance_dispo))
    montant_achat = float(input("Merci de renseigner le montant d'achat desirée en btc: "))  # BTC/ASK
    pourcent_ask = float(input("Merci de renseigner le pourcentage en plus du ask desirée(1.xx): "))
    pourcent_vente = float(input("Merci de renseigner le pourcentage de vente desirée(1.xx): "))
    market = input("Selectionner la crypto monnaie: ")
    marketbtc = "BTC-" + market
    rate_raw = my_bittrex.get_ticker(marketbtc)['result']['Ask']
    ratebuy = rate_raw * pourcent_ask
    ratesell = rate_raw * pourcent_vente
    quantity = montant_achat / rate_raw
    my_bittrex.buy_limit(marketbtc, quantity, ratebuy)
    time.sleep(0.6)
    while True:
        if loop_open_order(market, marketbtc) != "LIMIT_BUY":
            print("Achat effectué !!")
            break
    my_bittrex.sell_limit(marketbtc, quantity, ratesell)
    time.sleep(0.6)
    while True:
        if loop_open_order(market, marketbtc) != "LIMIT_SELL":
            print("Vente effectué !!")
            break
    input("Appuyer sur une touche pour continuer")
    balance_dispo = None
    montant_achat = None
    pourcent_ask = None
    pourcent_vente = None
    market = None
    marketbtc = None
    rate_raw = None
    ratebuy = None
    ratesell = None
    quantity = None


def sell():
    print("Sell order")
    market = input("Selectionner la crypto monnaie: ")
    marketbtc = "BTC-" + market
    balance_dispo = my_bittrex.get_balance(market)['result']['Balance']
    print("Voici la balance disponible: " + str(balance_dispo))
    quantity = float(input("Veuillez entrez la quantité a vendre: "))
    if quantity < balance_dispo:
        ask_test = input("Voulez vous vendre au taux 'Ask'? O/N: ")
        if ask_test == "O" or ask_test == "o":
            rate = my_bittrex.get_ticker(marketbtc)['result']['Ask']
        else:
            rate = float(input("Entrez le taux en BTC svp: "))
        print("Pair d'echange: " + marketbtc + " , Quantité: " + str(quantity) + " , Taux: " + str(rate))
        verif = input("Les données sont elle bonne?: ")
        if verif == "O" or verif == "o":
            my_bittrex.sell_limit(marketbtc, quantity, rate)
            print("Ordre de vente ouvert !")
    else:
        print("Merci d'entrer une quantité valide!")
    input("Appuyer sur une touche pour continuer")


def buy():
    print("Buy order")
    market = input("Selectionner la crypto monnaie: ")
    marketbtc = "BTC-" + market
    print("Voici la balance BTC disponible: " + str(my_bittrex.get_balance("BTC")['result']['Balance']))
    quantity = float(input("Veuillez entrez la quantité a acheter: "))
    balance_dispo = my_bittrex.get_balance("BTC")['result']['Balance']
    if quantity < balance_dispo:
        ask_test = input("Voulez vous acheter au taux 'Ask'? O/N: ")
        if ask_test == "O" or ask_test == "o":
            rate = my_bittrex.get_ticker(marketbtc)['result']['Ask']
        else:
            rate = float(input("Entrez le taux en BTC svp: "))
        print("Pair d'echange: " + marketbtc + " , Quantité: " + str(quantity) + " , Taux: " + str(rate))
        verif = input("Les données sont elle bonne?: ")
        if verif == "O" or verif == "o":
            my_bittrex.buy_limit(marketbtc, quantity, rate)
            print("ok")
    else:
        print("Merci d'entrer une quantité valide!")
    input("Appuyer sur une touche pour continuer")


def cancel():
    print("Cancel order")
    market = input("Selectionner la crypto monnaie: ")
    marketbtc = "BTC-" + market
    for i in range(len(my_bittrex.get_open_orders(marketbtc)['result'])):
        type_order = my_bittrex.get_open_orders(marketbtc)['result'][i]['OrderType']
        quantity_order = my_bittrex.get_open_orders(marketbtc)['result'][i]['Quantity']
        uuid_order = my_bittrex.get_open_orders(marketbtc)['result'][i]['OrderUuid']
        opened_date = my_bittrex.get_open_orders(marketbtc)['result'][i]['Opened']
        print(str(i + 1) + " order type: " + type_order + " , Quantity: " + str(
            quantity_order) + " , Uuid: " + str(uuid_order) + " , Date: " + str(opened_date))
        verif = input("Do you want to cancel an order? O/N")
        if verif == "O" or verif == "o":
            uuid_select = input("Paste the order uuid you want to cancel")
            my_bittrex.cancel(uuid_select)
    input("Appuyer sur une touche pour continuer")


def info():
    print("Load account info")
    market = input("Selectionner la crypto monnaie: ")
    get_balance = my_bittrex.get_balance(market)['result']['Balance']
    print(market + " amount: " + str(get_balance))
    marketbtc = "BTC-" + market
    for i in range(len(my_bittrex.get_open_orders(marketbtc)['result'])):
        type_order = my_bittrex.get_open_orders(marketbtc)['result'][i]['OrderType']
        quantity_order = my_bittrex.get_open_orders(marketbtc)['result'][i]['Quantity']
        uuid_order = my_bittrex.get_open_orders(marketbtc)['result'][i]['OrderUuid']
        opened_date = my_bittrex.get_open_orders(marketbtc)['result'][i]['Opened']
        print(str(i + 1) + " order type: " + type_order + " , Quantity: " + str(
            quantity_order) + " , Uuid: " + str(uuid_order) + " , Date: " + str(opened_date))
    input("Appuyer sur une touche pour continuer")
    market = None
    get_balance = None
    marketbtc = None
    type_order = None
    quantity_order = None
    uuid_order = None
    opened_date = None


def main():
    menu = CursesMenu("Bittrex_bot")
    pump_bot = FunctionItem("Pump", pump)
    sell_bot = FunctionItem("Sell", sell)
    buy_bot = FunctionItem("Buy", buy)
    cancel_bot = FunctionItem("Cancel", cancel)
    info_bot = FunctionItem("Info", info)
    menu.append_item(pump_bot)
    menu.append_item(sell_bot)
    menu.append_item(buy_bot)
    menu.append_item(cancel_bot)
    menu.append_item(info_bot)
    menu.start()
    menu.join()


main()
