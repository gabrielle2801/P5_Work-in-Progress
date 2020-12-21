from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Category, Product, Brand, Store
from off_client import OpenFoodFactsApi

global Session
engine = create_engine('postgresql://localhost/test')
Session = sessionmaker(bind=engine)


def add_store():
    client = OpenFoodFactsApi()
    stores = client.get_stores()
    for store in stores:
        store1 = Store(name=store)
        return store1
        print(store1)


def import_data():
    session = Session()
    client = OpenFoodFactsApi()
    categories = client.get_categories()
    stores = client.get_stores()
    # product_schema = ProductSchema()
    # insert data to Category
    for store in stores:
        store1 = Store(name=store)
        session.add(store1)
    for cat in categories:
        category1 = Category(name=cat)
        print(category1)
        products = client.get_products(cat)
        # insert data to Product, Store, Brand
        for product in products:
            if product.get("product_name") != "":
                b = session.query(Brand).filter(
                    Brand.name == product.get("brands")).first()
                if not b:
                    brand = Brand(name=product.get("brands"),
                                  label=product.get("label"))
                    session.add(brand)
                    b = session.query(Brand).filter(
                        Brand.name == product.get("brands")).first()
                    product = Product(name=product.get("product_name"),
                                      nutriscore=product.get(
                        "nutrition_grades"),
                        nova=product.get("nova_groups_tags"),
                        brand=b, url=product.get("url"),
                        barcode=product.get("code"))
                    product.categories.append(category1)
                    product.stores.append(store1)
                    print(product)
    session.add(product)
    session.commit()
    # dump_data = product_schema.dump(product)
    # load_data = product_schema.load(dump_data, session=session)
    session.close()
