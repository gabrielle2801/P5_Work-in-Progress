# from off_client import OpenFoodFactsApi
from import_db import Bdd


class Category_menu():

    def __init__(self):
        self.start()

    def start(self):
        bdd = Bdd()
        # client = OpenFoodFactsApi()
        # categories = client.get_categories()
        # print()
        entree = int(input(
            "1 - Quel aliment souhaitez-vous remplacer ? "'\n'"2 - Retrouver mes aliments substitués"'\n'))

        if entree == 1:
            i = 1
            j = 1
            for category in bdd.list_category:
                print(i, " - ", category)
                i = i + 1
            number_cat = int(input("Choississez la catégorie"'\n'))
            cat = bdd.list_category[number_cat - 1]
            print(cat)
            for product in bdd.get_product(cat):
                print(j, " - ", product.name)
                j = j + 1
            product_choice = int(
                input("Quel produit souhaitez-vous remplacer ?"'\n'))
            print(bdd.get_product(cat)[product_choice - 1])

        elif entree == 2:
            print("c'est fini ????")
