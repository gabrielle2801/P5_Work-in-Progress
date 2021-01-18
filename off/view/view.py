from constants import RESEARCH_BY_CATEGORY, SUBSTITUTES_LIST, HOMEPAGE, RESEARCH_BY_NAME
from constants import PRODUCTS_FOR_CATEGORY, PRODUCT_DETAIL, SAVE_SUBSTITUT
from constants import PRODUCTBYNAME_DETAIL, FOUND_PRODUCT, CATEGORYBYNAMELIST


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
        else:
            exit()


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
        print('\t'"Nutriscore : ", product.nutriscore)
        print('\t'"Nova group : ", product.nova)
        print('\t' "URL :", product.url)
        print('\t'"Stores :", stores, '\n')
        for id, substitute in enumerate(substituts):
            print(substitute.id, " - name of the substituts : ", substitute.name)
            print('\t'"Nutriscore :", substitute.nutriscore)
            print('\t' "Nova group :", substitute.nova)
            print('\t' "Description :", substitute.description)
            print('\t' "URL :", substitute.url)
            print('\t' "Stores : ", stores)

    def get_next_page(self):
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
                print(product.id, " - ", product.name)

    def get_next_page(self, products):
        if products == []:
            return RESEARCH_BY_NAME, None
        while True:
            try:
                product_choiced = int(input("Veuillez choisir le produit : "))
                break
            except ValueError:
                print("Oops!  Saisie invalide.  Essayez de nouveau...")
        return CATEGORYBYNAMELIST, product_choiced


class CategoriesByNameListView:

    def display(self, categories):
        print("Choix par catégorie")
        for id, category in enumerate(categories):
            print(category.id, " - ", category.name)

    def get_next_page(self):
        while True:
            try:
                category_choiced = int(input("Veuillez choisir la categorie "))
                break
            except ValueError:
                print("Oops!  Saisie invalide.  Essayez de nouveau...")
        return PRODUCTBYNAME_DETAIL, category_choiced

class ProductByNameDetailView:

    def display(self, product, substituts, stores):
        print(product.id, " - name of the product : ", product.name)
        print('\t'"Nutriscore : ", product.nutriscore)
        print('\t'"Nova group : ", product.nova)
        print('\t' "URL :", product.url)
        print('\t'"Stores :", stores, '\n')
        for id, substitute in enumerate(substituts):
            print(substitute.id, " - name of the substituts : ", substitute.name)
            print('\t'"Nutriscore :", substitute.nutriscore)
            print('\t' "Nova group :", substitute.nova)
            print('\t' "Description :", substitute.description)
            print('\t' "URL :", substitute.url)
            print('\t' "Store : ", stores)

    def get_next_page(self):
        while True:
            try:
                substitut_choice = int(
                    input("Quel substitut voulez vous sauvegarder ?"))
                break
            except ValueError:
                print("Oops!  Saisie invalide.  Essayez de nouveau...")
        return SAVE_SUBSTITUT, substitut_choice


class SubstituteListView:

    def display(self, products, substituts):
        print("Vos produits recherchés et leurs substitues trouvés : ")
        for id, (product, substitute) in enumerate(zip(products, substituts)):
            print(product.id, " - ", product.name, " -> ",
                  substitute.id, " - ", substitute.name)

    def get_next_page(self):
        while True:
            try:
                continued = input(
                    "Voulez vous chercher d'autres produits ? YES/NO"'\n')
                if continued == "YES":
                    return HOMEPAGE, continued
                elif continued == "NO":
                    print("Merci et à bientôt")
                    exit()
            except ValueError:
                print("Oops!  Saisie invalide.  Essayez de nouveau...")
        return SAVE_SUBSTITUT, continued
