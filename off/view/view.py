from constants import RESEARCH_BY_CATEGORY, SUBTITUTES_LIST, HOMEPAGE, RESEARCH_BY_NAME
from constants import PRODUCTS_FOR_CATEGORY, PRODUCT_DETAIL, SAVE_SUBTITUT, SUBTITUTES_RESEARCH


class HomepageView:

    def display(self):
        print("""
            1 - Chercher les subtituts du produit à remplacer !
            2 - Chercher par nom de produit à remplacer !
            3 - Retrouver mes aliments substitués
            """)

    def get_next_page(self):
        option = input("Que choissisez vous ?")
        if option == "1":
            return RESEARCH_BY_CATEGORY
        elif option == "2":
            return RESEARCH_BY_NAME
        elif option == "3":
            return SUBTITUTES_LIST
        else:
            return HOMEPAGE

class ProductByNameView:

    def display(self, products):
        product = input("Veuillez tapez le nom du produit : ")
        for id, product in enumerate(products):
            if product == product.name:
                print("Voici le produit trouvé ! : ",
                      product.id, " - ", product.name)
            elif product != product.name:
                print("Erreur de frappe veuillez recommencer !")
                return HOMEPAGE

    def get_next_page(self):
        product_by_name = input(
            "Voulez vous voir les subtitues proprosés ? YES/NO"'\n')
        if product_by_name == "YES":
            return PRODUCT_DETAIL, product_by_name
        if product_by_name == "NO":
            print("Merci et à bientôt")
            exit()

class ResearchListView:

    def display(self, products):
        print("Vos produits recherchés : ")
        for id, product in enumerate(products):
            print(product.id, " - ", product.name)

    def get_next_page(self):
        subtitute_research = input(
            "Voulez vous voir les produits de subtitutions associés ? YES/NO"'\n')
        if subtitute_research == "YES":
            return SUBTITUTES_RESEARCH, subtitute_research
        elif subtitute_research == "NO":
            print("Merci et à bientôt")
            exit()


class SubtituteListView:

    def display(self, subtituts):
        print("les produits ont été subtitués par : ")
        for id, subtitut in enumerate(subtituts):
            print(subtitut.id, " - ", subtitut.name)

    def get_next_page(self):
        product_research = input(
            "Voulez vous chercher d'autres produits à subtitués ? YES/NO"'\n')
        if product_research == "YES":
            return RESEARCH_BY_CATEGORY, product_research
        elif product_research == "NO":
            print("Merci et à bientôt")
            exit()


class CategoryListView:

    def display(self, categories):

        for id, category in enumerate(categories):
            print(category.id, " - ", category.name)

    def get_next_page(self):
        category_id = int(input("Choississez la catégorie"'\n'))
        return PRODUCTS_FOR_CATEGORY, category_id


class ProductByCategoryView:

    def display(self, products):
        for id, product in enumerate(products):
            print(product.id, " - ", product.name)

    def get_next_page(self):
        product_id = int(
            input("Quel produit souhaitez-vous remplacer ?"'\n'))
        return PRODUCT_DETAIL, product_id


class ProductDetailView:

    def display(self, product, subtituts, stores):
        print(product.id, " - name of the product : ", product.name)
        print('\t'"Nutriscore : ", product.nutriscore)
        print('\t'"Nova group : ", product.nova)
        print('\t'"Stores :", stores, '\n')
        for id, subtitute in enumerate(subtituts):
            print(subtitute.id, " - name of the subtituts : ", subtitute.name)
            print('\t'"Nutriscore :", subtitute.nutriscore)
            print('\t' "Nova group :", subtitute.nova)
            print('\t' "Description :", subtitute.description)
            print('\t' "Store : ", stores)

    def get_next_page(self):
        subtitut_choice = int(input("Quel subtitut voulez vous sauvegarder ?"))
        return SAVE_SUBTITUT, subtitut_choice
