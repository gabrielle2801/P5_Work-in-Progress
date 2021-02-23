from off.model.db.models import Product, Base
from off.model.query.manager import DBManager
from off.model.api.off_client import OpenFoodFactsApi
from off.constants import DB_ENGINE_URL
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, create_database


class Database:
    def __init__(self):
        self.openFoodFactsApi = OpenFoodFactsApi()
        self.create_database()
        self.create_tables()
        self.import_data()

    def create_database(self):
        '''
        This function create database 'off_db'
        Parameters :
            DB_ENGINE_URL :'postgresql://postgres:purbeurre@localhost:5432/off_db'
        Returns :
            create_database : create the DB with engine.url
        '''
        print("Création de la Base de Données...")
        engine = create_engine(DB_ENGINE_URL)
        if not database_exists(engine.url):
            create_database(engine.url)

        print(database_exists(engine.url))

    def create_tables(self):
        '''
        This Function create tables on database 'off_db'.
        Parameters :
            Class Product : main table 'product' has attributes as
                            * id : primary key
                            * name
                            * nutriscore : A to E
                            * nova : 1 tp 4
                            * url : link to detail product on OFF
                            * barcode
                            * description : ingredients detail
                            * brand_id = many to one relationship Foreign key
            Class Brand :  table 'brand' many to one (product -> brand)
                            * id : primary key
                            * name
                            * label

            Class Store : table 'store' many to many relationship
                            * id : primary key
                            * name
            Class product_store : many to many (product -> store)
                            * product_id : Foreign key
                            * store_id : Foreign key
            Class Category : table 'category' many to many relationship
                            * id : primary key
                            * name
            Class product_category : many to many (product -> category)
                            * product_id
                            * category_id
            Class Substitut : table 'substitute'
                            one to many (product -> substitute)
                            * id : primary key
                            * product_id : Foreign key
                            * substitute_id : Foreign key
        Returns :
            create engine ('postgresql://postgres:purbeurre@localhost:5432/off_db')
            create a session
            create_all : create tables on dayabse 'off_db' '''
        print("Création des Tables ...")
        global Session
        engine = create_engine(DB_ENGINE_URL)
        Session = sessionmaker(bind=engine)
        Base.metadata.create_all(engine)

    def import_data(self):
        '''
        This Function insert data on 'off_db'
        This function get and insert categories and products on a list
        with OpenFoodFactsApi class based on off_client.py.
        the method used is get_categories and get_products.
        '''
        self.list_category = self.OpenFoodFactsApi.get_categories()
        manager = DBManager()
        for category in self.list_category:
            products = self.openFoodFactsApi.get_products(category)
            # insert data to Product, Store, Brand
            for product in products:
                if (not product.get("product_name")
                    or not product.get("nutrition_grades") or
                        manager.session.query(Product).filter(
                            Product.barcode == product.get("code")).first()
                        is not None):

                    continue
                if product.get("labels"):
                    brand_insert = manager.get_or_create_brand(product.get(
                        "brands"), product.get("labels").split(","))
                else:
                    brand_insert = manager.get_or_create_brand(product.get(
                        "brands"), "")

                product_data = Product(
                    name=product.get("product_name"),
                    nutriscore=product.get("nutrition_grades"),
                    nova=product.get("nova_group"),
                    url=product.get("url"),
                    description=product.get("ingredients_text"),
                    barcode=product.get("code"),
                    brand=brand_insert)

                category_names = product.get("categories").split(",")
                for category in category_names:
                    categories = manager.get_or_create_category(category)
                    product_data.categories.append(categories)

                if product.get("stores"):
                    store_names = product.get("stores").split(",")
                    for store in store_names:
                        stores = manager.get_or_create_store(store)
                        product_data.stores.append(stores)

                manager.session.add(product_data)
        manager.session.commit()
        manager.session.close()
