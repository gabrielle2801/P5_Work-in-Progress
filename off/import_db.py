from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Category, Product, Brand, Store, product_store
from off_client import OpenFoodFactsApi

global Session
engine = create_engine('postgresql://localhost/off_db')
Session = sessionmaker(bind=engine)


def import_data():
    session = Session()
    client = OpenFoodFactsApi()
    categories = client.get_categories()
    # insert data to Category
    for cat in categories:
        products = client.get_products(cat)
        session.add(Category(name=cat))
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
                session.add(Product(name=product.get("product_name"),
                                    nutriscore=product.get(
                    "nutrition_grades"),
                    nova=product.get("nova_groups_tags"),
                    brand=b, url=product.get("url"),
                    barcode=product.get("code")))
    stores = client.get_stores()
    for store in stores:
        session.add(Store(name=store))
    p = session.query(Product).filter(
        Product.name == product.get("products")).first()
    s = session.query(Store).filter(
        Store.name == store.get("stores")).first()
    session.add(product_store(id_product=p, id_store=s))

    session.commit()
    session.close()
