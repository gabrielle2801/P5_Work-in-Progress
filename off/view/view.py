from constants import RESEARCH_BY_CATEGORY, SUBSTITUTES_LIST, HOMEPAGE
from constants import PRODUCTS_FOR_CATEGORY, PRODUCT_DETAIL, SAVE_SUBSTITUT
from constants import FOUND_PRODUCT, RESEARCH_BY_NAME
import os


class HomepageView:

    def display(self):
        print("""
            Bienvenue sur le programme PurBeurre !
            Ce programme vous permet de trouver des aliments de meilleurs qualités
            1 - Chercher les substituts du produit à remplacer par catégorie !
            2 - Chercher par nom de produit à remplacer !
            3 - Retrouver mes aliments substitués
            4 - Quitter
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
            exit()
            os.system('clear')


class CategoryListView:

    def display(self, categories):

        for id, category in enumerate(categories):
            print(category.id, " - ", category.name)

    def get_next_page(self):
        while True:
            try:
                category_id = int(input("Choississez la catégorie"'\n'))
                break
            except ValueError:
                print("Oops!  Saisie invalide.  Essayez de nouveau...")
        return PRODUCTS_FOR_CATEGORY, category_id


class ProductByCategoryView:

    def display(self, products):
        for id, product in enumerate(products):
            print(product.id, " - ", product.name)

    def get_next_page(self):
        while True:
            try:
                product_id = int(
                    input("Quel produit souhaitez-vous remplacer ?"'\n'))
                break
            except ValueError:
                print("Oops!  Saisie invalide.  Essayez de nouveau...")
        return PRODUCT_DETAIL, product_id


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
                print(substitute.id, " - name of the substituts : ", substitute.name)
                print('\t'"Nutriscore :", substitute.nutriscore.upper())
                print('\t' "Nova group :", substitute.nova)
                print('\t' "Description :", substitute.description)
                print('\t' "URL :", substitute.url)
                print('\t' "Stores : ", stores)

    def get_next_page(self, substituts):
        if substituts == []:
            # homepage = input("tapez h pour revenir à la page principale"'\n')
            return HOMEPAGE, None
        while True:
            try:
                substitut_choice = int(
                    input("Quel substitut voulez vous sauvegarder ?"'\n'))
                break
            except ValueError:
                print("Oops!  Saisie invalide.  Essayez de nouveau...")
        return SAVE_SUBSTITUT, substitut_choice


class ProductByNameView:

    def display(self):
        print("Recherche par nom de produit ")

    def get_next_page(self):
        product_name = input("Veuillez tapez le nom du produit : ")
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
                product_choiced = int(input("Veuillez choisir le produit : "))
                break
            except ValueError:
                print("Oops!  Saisie invalide.  Essayez de nouveau...")
        return PRODUCT_DETAIL, product_choiced


class ProductByNameDetailView:

    def display(self, product, substituts, stores):
        print(product.id, " - name of the product : ", product.name)
        print('\t'"Nutriscore : ", product.nutriscore)
        print('\t'"Nova group : ", product.nova)
        print('\t' "URL :", product.url)
        print('\t'"Stores :", stores, '\n')
        if substituts == []:
            print("pas de substituts trouvés !")
        else:
            for id, substitute in enumerate(substituts):
                print(substitute.id, " - name of the substituts : ", substitute.name)
                print('\t'"Nutriscore :", substitute.nutriscore.upper())
                print('\t' "Nova group :", substitute.nova)
                print('\t' "Description :", substitute.description)
                print('\t' "URL :", substitute.url)
                print('\t' "Store : ", stores)

    def get_next_page(self, substituts):
        if substituts == []:
            # homepage = input("tapez h pour revenir à la page principale"'\n')
            return HOMEPAGE, None
        while True:
            try:
                substitut_choice = int(
                    input("Quel substitut voulez vous sauvegarder ?"))
                break
            except ValueError:
                print("Oops!  Saisie invalide.  Essayez de nouveau...")
        return SAVE_SUBSTITUT, substitut_choice


class SubstituteListView:

    def display(self, substituts):
        print("Vos produits recherchés et leurs substitues trouvés : ")
        for substitute in substituts:
            print(substitute.product.id, substitute.product,
                  " -> ", substitute.subtitute)

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
