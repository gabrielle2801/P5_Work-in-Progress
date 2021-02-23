from off.constants import RESEARCH_BY_CATEGORY, SUBSTITUTES_LIST, HOMEPAGE,\
    PRODUCTS_FOR_CATEGORY, PRODUCT_DETAIL, SAVE_SUBSTITUT,\
    FOUND_PRODUCT, RESEARCH_BY_NAME, PRODUCT_REMINDER
import os

class GenericView:

    ''' This class handle errors exceptions
    '''
    input_error_msg = "Oops!  Saisie invalide.  Essayez de nouveau..."

    def valid_numeric_and_home(self, value):
        return value.isnumeric() or value.lower() == "h"

class HomepageView(GenericView):

    def display(self):
        print("""
            Bienvenue sur le programme PurBeurre !
            Ce programme vous permet de trouver des aliments de meilleurs
            qualités
            1 - Chercher les substituts du produit à remplacer par catégorie !
            2 - Chercher par nom de produit à remplacer !
            3 - Retrouver mes aliments substitués
            4 - Quitter
            Pour revenir au menu principal -> tapez h à tout moment
            """)

    def get_next_page(self):
        while True:
            value = input("Que choissisez vous ?")
            if not self.valid_numeric_and_home(value):
                print(self.input_error_msg)
                continue

            if value == "1":
                return RESEARCH_BY_CATEGORY
            elif value == "2":
                return RESEARCH_BY_NAME
            elif value == "3":
                return SUBSTITUTES_LIST
            elif value == "4":
                print("Merci et à bientôt")
                os.system('clear')
                exit()
            else:
                print("Erreur de saisie")


class CategoryListView(GenericView):

    def display(self, categories):

        for id, category in enumerate(categories):
            print(category.id, " - ", category.name)

    def get_next_page(self):
        while True:
            value = input("Choississez la catégorie"'\n')
            if not self.valid_numeric_and_home(value):
                print(self.input_error_msg)
                continue

            if value.lower() == "h":
                return HOMEPAGE, None
            try:
                return PRODUCTS_FOR_CATEGORY, int(value)
            except Exception:
                pass


class ProductByCategoryView(GenericView):

    def display(self, products):
        for id, product in enumerate(products):
            print(product.id, " - ", product)

    def get_next_page(self):
        while True:
            value = input(
                "Quel produit souhaitez-vous remplacer ?"'\n')

            if not self.valid_numeric_and_home(value):
                print(self.input_error_msg)
                continue

            if value.lower() == "h":
                return HOMEPAGE, None
            try:
                return PRODUCT_DETAIL, int(value)
            except Exception:
                pass


class ProductDetailView(GenericView):

    def display(self, product, substituts, stores_product, stores_substitutes):
        print(product.id, " - name of the product : ", product.name)
        print('\t'"Nutriscore : ", product.nutriscore.upper())
        print('\t'"Nova group : ", product.nova)
        print('\t' "URL :", product.url)
        print('\t'"Stores :", stores_product, '\n')
        if substituts == []:
            print("pas de substituts trouvés !")
        else:
            for id, substitute in enumerate(substituts):
                print(substitute.id, " - name of the substituts : ",
                      substitute.name)
                print('\t'"Nutriscore :", substitute.nutriscore.upper())
                print('\t' "Nova group :", substitute.nova)
                print('\t' "Description :", substitute.description)
                print('\t' "URL :", substitute.url)
                print('\t' "Stores : ", stores_substitutes[id])

    def get_next_page(self, substituts):
        while True:
            if substituts == []:
                return HOMEPAGE, None
            value = \
                input("Quel substitut voulez vous sauvegarder ?"'\n')

            if not self.valid_numeric_and_home(value):
                print(self.input_error_msg)
                continue
            if value.lower() == "h":
                return HOMEPAGE, None
            try:
                return SAVE_SUBSTITUT, int(value)
            except Exception:
                pass


class ProductByNameView(GenericView):

    def display(self):
        print("Recherche par nom de produit ")

    def get_next_page(self):
        while True:
            value = input("Veuillez tapez le nom du produit : ")
            if value.lower() == "h":
                return HOMEPAGE, None, None
            else:
                return FOUND_PRODUCT, value, None


class ProductByNameListView(GenericView):
    def display(self, products):
        if products == []:
            print("Produit non trouvé !")
        else:
            print("Produits trouvés : ")
            for id, product in enumerate(products):
                print(product.id, " - ", product)

    def get_next_page(self, products):
        while True:
            if products == []:
                return RESEARCH_BY_NAME, None
            value = input("Veuillez choisir le produit : ")
            if not self.valid_numeric_and_home(value):
                print(self.input_error_msg)
                continue
            if value.lower() == "h":
                return HOMEPAGE, None
            try:
                return PRODUCT_DETAIL, int(value)
            except Exception:
                pass


class SubstituteListView(GenericView):

    def display(self, substituts):
        print("Vos produits recherchés et leurs substitues trouvés : ")
        for substitute in substituts:
            print(substitute.product.id, substitute.product,
                  " -> ", substitute.substitute)

    def get_next_page(self, products):
        while True:
            value =\
                input("Voulez-vous revoir un produit sauvegardé ? : yes/no"
                      '\n')
            if value.lower() == "h" or value.lower() == "no":
                return HOMEPAGE, None
            if value.lower() == "yes":
                product_reminder = input(
                    "Veuillez choisir le produit à revoir : ")
            if not self.valid_numeric_and_home(product_reminder):
                print(self.input_error_msg)
                continue
            try:
                return PRODUCT_REMINDER, int(product_reminder)
            except Exception:
                pass


class ProductReminderView(GenericView):

    def display(self, product, stores):
        print("Vous desirez revoir le produit : ")
        print("name of the product : ", product.name)
        print('\t'"Nutriscore : ", product.nutriscore.upper())
        print('\t'"Nova group : ", product.nova)
        print('\t' "URL :", product.url)
        print('\t'"Stores :", stores, '\n')

    def get_next_page(self):
        value = input(
            "Voulez vous chercher d'autres produits ? yes/no"'\n')
        if value.lower() == "yes":
            return HOMEPAGE, value
        elif value.lower() == "no":
            print("Merci et à bientôt")
            os.system('clear')
            exit()
        return SAVE_SUBSTITUT, value
