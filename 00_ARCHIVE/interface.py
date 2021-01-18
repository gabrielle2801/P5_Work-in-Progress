# from off_client import OpenFoodFactsApi
from import_db import Database
from manager import Productbycategory


class Category_menu():

    def __init__(self):
        self.start()

    def start(self):
        bdd = Database()
        menu = Productbycategory()
        entree = int(input(
            "1 - Quel aliment souhaitez-vous remplacer ? "'\n'"2 - Retrouver mes aliments substitués"'\n'))

        if entree == 1:
            i = 1
            j = 1
            for category in bdd.list_category:
                print(i, " - ", category)
                i = i + 1
            number_category = int(input("Choississez la catégorie"'\n'))
            categories = bdd.list_category[number_category - 1]
            print(categories)
            for product in menu.get_product(categories):
                print(j, " - ", product.name)
                j = j + 1
            product_choice = int(
                input("Quel produit souhaitez-vous remplacer ?"'\n'))
            print(menu.get_product(categories)[product_choice - 1])
            for subtitute in menu.get_subtitute(product, categories):
                print(subtitute.name, subtitute.nutriscore)
                for store in menu.get_store(subtitute):
                    print(store.name)

        elif entree == 2:
            print("c'est fini ????")
