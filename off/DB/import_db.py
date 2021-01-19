# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker
from DB.models import Product, Store
from query.manager import DBManager
from off_client import OpenFoodFactsApi

global Session
# engine = create_engine('postgresql://localhost/test')
# Session = sessionmaker(bind=engine)


class Database:
    def __init__(self):
        # self.session = Session()
        self.openFoodFactsApi = OpenFoodFactsApi()
        self.list_category = self.openFoodFactsApi.get_categories()
        self.import_data()

    def import_data(self):
        manager = DBManager()
        for category in self.list_category:
            products = self.openFoodFactsApi.get_products(category)
            # insert data to Product, Store, Brand
            for product in products:
                if not product.get("product_name") or \
                        manager.session.query(Product).filter(
                            Product.barcode == product.get("code")).first()\
                        is not None:

                    continue
                brand_insert = manager.get_or_create_brand(product.get(
                    "brands"), product.get("labels").split(","))

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
                for store_name in product.get("stores").split(","):
                    store = manager.session.query(Store).filter(
                        Store.name == store_name).first()
                    if not store:
                        store = Store(name=store_name)
                    product_data.stores.append(store)

                # product_data.categories.append(categories)
                manager.session.add(product_data)
        manager.session.commit()
        manager.session.close()
