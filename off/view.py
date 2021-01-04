from models import Subtitute
from constants import RECHERCHE_PAR_CATEGORY, ALIMENTS_SUBTITUES, HOMEPAGE
from constants import PRODUCT, DETAIL_PRODUCT, SAVE_SUBTITUT
from manager import Productbycategory
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

global Session
engine = create_engine('postgresql://localhost/test')
Session = sessionmaker(bind=engine)
class HomepageView:

    def display(self):
        print("""
            1 - Quel aliment souhaitez-vous remplacer ?
            2 - Retrouver mes aliments substitués
            """)

    def get_next_page(self):
        option = input("Que choissisez vous ?")
        if option == "1":
            return RECHERCHE_PAR_CATEGORY
        elif option == "2":
            return ALIMENTS_SUBTITUES
        else:
            return HOMEPAGE


class Category:

    def display(self):
        menu = Productbycategory()
        # bdd = Database()
        i = 1
        for category in menu.get_category():
            print(i, " - ", category.name)
            i += 1

    def get_next_page(self):
        # bdd = Database()
        menu = Productbycategory()
        number_category = int(input("Choississez la catégorie"'\n'))
        category = menu.get_category()[number_category - 1]
        return PRODUCT, category


class ProductbyCategory:

    def display(self, category):
        menu = Productbycategory()
        j = 1
        for product in menu.get_product(category):
            print(j, " - ", product.name)
            j += 1

    def get_next_page(self, category):
        menu = Productbycategory()
        choice = int(
            input("Quel produit souhaitez-vous remplacer ?"'\n'))
        product_choice = menu.get_product(category)[choice - 1]
        return DETAIL_PRODUCT, product_choice


class Detail_product:

    def display(self, product, category):
        menu = Productbycategory()
        store = self.store_data(product)
        k = 1
        print("Name of product : ", product.name, '\n', "Nutriscore: ", product.nutriscore,
              '\n', "Stores : ", store, '\n', '\n', '\n',)
        for subtitute in menu.get_subtitute(product, category):
            print(k, " - "'\t'"Subtitute : ", subtitute.name, '\n',
                  '\t'"Nutriscore : ", subtitute.nutriscore, '\n',
                  '\t'"description : ", subtitute.description, '\n',
                  '\t'"url : ", subtitute.url, '\n'
                  '\t'"Stores : ", store, '\n', '\n',
                  "----------------------------------------------------------------------")
            k += 1

    def store_data(self, product):
        menu = Productbycategory()
        result_store = ""
        for store in menu.get_store(product):
            result_store += store.name
            result_store += ", "
        return result_store

    def save_subtitute(self, name, nutriscore, description, url, store):
        self.session = Session()
        subtitute = self.session.query(Subtitute).filter(
            Subtitute.name == name).first()
        if not subtitute:
            subtitute = Subtitute(name=name, nutriscore=nutriscore,
                                  description=description, url=url, store=store)
            self.session.add(subtitute)
        return subtitute
        subtitute_data = Subtitute(name=subtitute.name,
                                   nutriscore=subtitute.nutriscore,
                                   description=subtitute.description,
                                   url=subtitute.url,
                                   store=store.name)
        subtitute_data.products.append(subtitute)

    def get_next_page(self, subtitute, name, nutriscore, description, store, url):
        subtitute_save = self.save_subtitute(
            name, nutriscore, description, store, url)
        subtitute_menu = input(
            "souhaitez-vous enregistrer votre choix dans votre liste ? Y/N"'\n')
        if subtitute_menu == "Y":
            number_subtitute = int(
                input("Que choissisez vous comme subtitut à sauvegarder"'\n'))
            subtitute_choice = subtitute_save.save_subtitute(subtitute.name,
                                                             subtitute.nutriscore,
                                                             subtitute.description,
                                                             subtitute.store,
                                                             subtitute.url)[number_subtitute - 1]
            return SAVE_SUBTITUT, subtitute_choice
        elif subtitute_menu == "N":
            print("Merci et à bientôt")
            return exit()


class Subtitut:

    def display(self, subtitute, name, nutriscore, description, store, url):
        print("Subtitut sauvegardé ! Pour voir les subtituts allez dans\
                        le menu principal")

    def get_next_page(self):
        keep_on = input("Voulez vous chercher un autre subtitut ? Y/N")
        if keep_on == "Y":
            return HOMEPAGE
        elif keep_on == "N":
            print("Merci et à bientôt")
            return exit()
