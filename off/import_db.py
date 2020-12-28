from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Category, Product, Brand, Store, Subtitute
from off_client import OpenFoodFactsApi

global Session
engine = create_engine('postgresql://localhost/test')
Session = sessionmaker(bind=engine)


class Bdd:
    def __init__(self):
        self.session = Session()
        self.openFoodFactsApi = OpenFoodFactsApi()
        self.list_category = self.openFoodFactsApi.get_categories()
        self.import_data()
        # self.create_substitute()

    def get_or_create_brand(self, brand_name, label):

        brand = self.session.query(Brand).filter(
            Brand.name == brand_name).first()
        if not brand:
            brand = Brand(name=brand_name, label=label)
            # print(brand)
            self.session.add(brand)
        return brand

    def import_data(self):
        #self.session = Session()
        #client = OpenFoodFactsApi()
        #categories = client.get_categories()

        for category in self.list_category:
            category_name = Category(name=category)
            subtitutes = self.openFoodFactsApi.get_producthealthy(category)
            products = self.openFoodFactsApi.get_products(category)
            # insert data to Product, Store, Brand
            for product in products:
                if not product.get("product_name") or \
                    self.session.query(Product).filter(Product.barcode ==
                                                       product.get("code")).first():
                    continue
                brand_insert = self.get_or_create_brand(product.get(
                    "brands"), product.get("labels").split(","))
                product_data = Product(
                    name=product.get("product_name"),
                    nutriscore=product.get("nutrition_grades"),
                    nova=product.get("nova_groups_tags"),
                    url=product.get("url"),
                    barcode=product.get("code"),
                    brand=brand_insert)

                for store_name in product.get("stores").split(","):
                    store = self.session.query(Store).filter(
                        Store.name == store_name).first()
                    # print(store)
                    if not store:
                        store = Store(name=store_name)
                    product_data.stores.append(store)
                product_data.categories.append(category_name)
                self.session.add(product_data)
            for healthy in subtitutes:
                if not healthy.get("product_name"):
                    continue
                self.session.add(Subtitute(
                    name=healthy.get("product_name"),
                    description=healthy.get("ingredients"),
                    store=healthy.get("stores"),
                    url=healthy.get("url")
                ))
        self.session.commit()
        # self.session.close()

    def create_substitute(self):
        #self.session = Session()
        #client = OpenFoodFactsApi()
        #categories = client.get_categories()
        for category in self.list_category:
            subtitutes = self.openFoodFactsApi.get_producthealthy(category)
            category_name = Category(name=category)
            print(category_name)
            # insert data to Product, Store, Brand
            for healthy in subtitutes:
                if not healthy.get("product_name"):
                    continue
                self.session.add(Subtitute(
                    name=healthy.get("product_name"),
                    description=healthy.get("ingredients"),
                    store=healthy.get("stores"),
                    url=healthy.get("url")
                ))
                # healthy.categories.append(category_name)
                # self.session.add(healthy)
        self.session.commit()
        self.session.close()

    def get_product(self, category):
        return self.session.query(Product.name).select_from(Category)\
            .join(Product.categories).filter(Category.name == category).all()
