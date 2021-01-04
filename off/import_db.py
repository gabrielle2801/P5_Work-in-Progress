from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Category, Product, Brand, Store, Subtitute
from off_client import OpenFoodFactsApi

global Session
engine = create_engine('postgresql://localhost/test')
Session = sessionmaker(bind=engine)


class Database:
    def __init__(self):
        self.session = Session()
        self.openFoodFactsApi = OpenFoodFactsApi()
        self.list_category = self.openFoodFactsApi.get_categories()
        self.import_data()

    def get_or_create_brand(self, brand_name, label):

        brand = self.session.query(Brand).filter(
            Brand.name == brand_name).first()
        if not brand:
            brand = Brand(name=brand_name, label=label)
            self.session.add(brand)
        return brand

def save_subtitute(self, name, nutriscore, description, store, url):

        subtitute = self.session.query(Subtitute).filter(
            Subtitute.name == name).first()
        if not subtitute:
            subtitute = Subtitute(name=name, nutriscore=nutriscore,
                                  description=description, store=store, url=url)
            self.session.add(subtitute)
        return subtitute
        subtitute_data = Subtitute(name=subtitute.name,
                                   nutriscore=subtitute.nutriscore,
                                   description=subtitute.description,
                                   url=subtitute.url,
                                   store=store.name)
        subtitute_data.products.append(subtitute)


    def import_data(self):

        for category in self.list_category:
            print(len(self.list_category))
            # print(category)
            category_name = Category(name=category)
            products = self.openFoodFactsApi.get_products(category)
            # insert data to Product, Store, Brand
            for product in products:
                print("produit    ", self.session.query(Product).filter(
                    Product.barcode == product.get("code")).first())

                print("le nom du produit   ", product.get("product_name"))
                if not product.get("product_name") or \
                        self.session.query(Product).filter(
                            Product.barcode == product.get("code")).first()\
                        is not None:

                    continue
                brand_insert = self.get_or_create_brand(product.get(
                    "brands"), product.get("labels").split(","))
                product_data = Product(
                    name=product.get("product_name"),
                    nutriscore=product.get("nutrition_grades"),
                    nova=product.get("nova_group"),
                    url=product.get("url"),
                    description=product.get("ingredients_text"),
                    barcode=product.get("code"),
                    brand=brand_insert)
                # print(product_data)
                for store_name in product.get("stores").split(","):
                    store = self.session.query(Store).filter(
                        Store.name == store_name).first()
                    if not store:
                        store = Store(name=store_name)
                    product_data.stores.append(store)
                product_data.categories.append(category_name)
                self.session.add(product_data)
        self.session.commit()
        self.session.close()
