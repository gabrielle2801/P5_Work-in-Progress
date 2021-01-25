from constants import RESEARCH_BY_CATEGORY, SUBSTITUTES_LIST, HOMEPAGE
from constants import PRODUCTS_FOR_CATEGORY, PRODUCT_DETAIL, SAVE_SUBSTITUT
from constants import FOUND_PRODUCT, RESEARCH_BY_NAME, PRODUCT_REMINDER
import os


class HomepageView:

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
        option = input("Que choissisez vous ?")
        if option == "1":
            return RESEARCH_BY_CATEGORY
        elif option == "2":
            return RESEARCH_BY_NAME
        elif option == "3":
            return SUBSTITUTES_LIST
        elif option == "4":
            print("Merci et à bientôt")
            os.system('clear')
            exit()


class CategoryListView:

    def display(self, categories):

        for id, category in enumerate(categories):
            print(category.id, " - ", category.name)

    def get_next_page(self):
        while True:
            try:
                category_id = input("Choississez la catégorie"'\n')
                if category_id == "h":
                    return HOMEPAGE, None
                else:
                    return PRODUCTS_FOR_CATEGORY, category_id
                break
            except ValueError:
                print("Oops!  Saisie invalide.  Essayez de nouveau...")


class ProductByCategoryView:

    def display(self, products):
        for id, product in enumerate(products):
            print(product.id, " - ", product.name)

    def get_next_page(self):
        while True:
            try:
                product_id = input(
                    "Quel produit souhaitez-vous remplacer ?"'\n')
                if product_id == "h":
                    return HOMEPAGE, None
                else:
                    return PRODUCT_DETAIL, product_id
                break
            except ValueError:
                print("Oops!  Saisie invalide.  Essayez de nouveau...")


class ProductDetailView:

    def display(self, product, substituts, stores):
        print(product.id, " - name of the product : ", product.name)
        print('\t'"Nutriscore : ", product.nutriscore.upper())
        print('\t'"Nova group : ", product.nova)
        print('\t' "URL :", product.url)
        print('\t'"Stores :", stores, '\n')
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
                print('\t' "Stores : ", stores)

    def get_next_page(self, substituts):
        if substituts == []:
            return HOMEPAGE, None
        while True:
            try:
                substitut_choice = \
                    input("Quel substitut voulez vous sauvegarder ?"'\n')
                if substitut_choice == "h":
                    return HOMEPAGE, None
                else:
                    return SAVE_SUBSTITUT, substitut_choice
                break
            except ValueError:
                print("Oops!  Saisie invalide.  Essayez de nouveau...")


class ProductByNameView:

    def display(self):
        print("Recherche par nom de produit ")

    def get_next_page(self):
        product_name = input("Veuillez tapez le nom du produit : ")
        if product_name == "h":
            return HOMEPAGE, None
        else:
            return FOUND_PRODUCT, product_name


class ProductByNameListView:
    def display(self, products):
        if products == []:
            print("Produit non trouvé !")
        else:
            print("Produits trouvés : ")
            for id, product in enumerate(products):
                print(product.id, " - ", product)

    def get_next_page(self, products):
        if products == []:
            return RESEARCH_BY_NAME, None
        while True:
            try:
                product_choiced = input("Veuillez choisir le produit : ")
                if product_choiced == "h":
                    return HOMEPAGE, None
                else:
                    return PRODUCT_DETAIL, product_choiced
                break
            except ValueError:
                print("Oops!  Saisie invalide.  Essayez de nouveau...")


class ProductByNameDetailView:

    def display(self, product, substituts, stores):
        print(product.id, " - name of the product : ", product.name)
        print('\t'"Nutriscore : ", product.nutriscore.upper())
        print('\t'"Nova group : ", product.nova)
        print('\t' "URL :", product.url)
        print('\t'"Stores :", stores, '\n')
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
                print('\t' "Store : ", stores)

    def get_next_page(self, substituts):
        if substituts == []:
            return HOMEPAGE, None
        while True:
            try:
                substitut_choice = \
                    input("Quel substitut voulez vous sauvegarder ?")
                if substitut_choice == "h":
                    return HOMEPAGE, None
                else:
                    os.system('clear')
                    return SAVE_SUBSTITUT, substitut_choice
                break
            except ValueError:
                print("Oops!  Saisie invalide.  Essayez de nouveau...")


class SubstituteListView:

    def display(self, substituts):
        print("Vos produits recherchés et leurs substitues trouvés : ")
        for substitute in substituts:
            print(substitute.product.id, substitute.product,
                  " -> ", substitute.substitute)

    def get_next_page(self, products):
        while True:
            try:
                reminder_choice =\
                    input("Voulez-vous revoir un produit sauvegardé ? : YES/NO"
                          '\n')
                if reminder_choice == "h":
                    return HOMEPAGE, None
                elif reminder_choice == "YES":
                    product_reminder = input(
                        "Veuillez choisir le produit à revoir : ")
                    return PRODUCT_REMINDER, product_reminder
                elif reminder_choice == "NO":
                    return HOMEPAGE, None
                break
            except ValueError:
                print("Oops!  Saisie invalide.  Essayez de nouveau...")


class ProductReminderView:

    def display(self, product, stores):
        print("Vous desirez revoir le produit : ")
        print("name of the product : ", product.name)
        print('\t'"Nutriscore : ", product.nutriscore.upper())
        print('\t'"Nova group : ", product.nova)
        print('\t' "URL :", product.url)
        print('\t'"Stores :", stores, '\n')

    def get_next_page(self):
        while True:
            try:
                continued = input(
                    "Voulez vous chercher d'autres produits ? YES/NO"'\n')
                if continued == "YES":
                    return HOMEPAGE, continued
                elif continued == "NO":
                    print("Merci et à bientôt")
                    os.system('clear')
                    exit()

            except ValueError:
                print("Oops!  Saisie invalide.  Essayez de nouveau...")
        return SAVE_SUBSTITUT, continued
