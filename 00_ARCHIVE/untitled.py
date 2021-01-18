from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Category, Product, Brand, Store
from off_client import OpenFoodFactsApi

global Session
engine = create_engine('postgresql://localhost/test')
Session = sessionmaker(bind=engine)


def get_or_create_brand(session, brand_name, label):

    brand = session.query(Brand).filter(
        Brand.name == brand_name).first()
    print(brand)
    if not brand:
        brand = Brand(name=brand_name, label=label)
        session.add(brand)
    return brand


def import_data():
    session = Session()
    client = OpenFoodFactsApi()
    categories = client.get_categories()

    for category in categories:
        category_name = Category(name=category)
        products = client.get_products(category)
        # insert data to Product, Store, Brand
        for product in products:
            p = session.query(Product).filter(
                Product.name == product.get("product_name")).first()
            print(p)
            if not product.get("product_name"):
                continue
            brand_insert = get_or_create_brand(session, product.get("brands"),
                                               product.get("label"))
            product_data = Product(
                name=product.get("product_name"),
                nutriscore=product.get("nutrition_grades"),
                nova=product.get("nova_groups_tags"),
                url=product.get("url"),
                barcode=product.get("code"),
                brand=brand_insert)

            for store_name in product.get("stores").split(","):
                store = Store(name=store_name)
                product_data.stores.append(store)
            product_data.categories.append(category_name)
        session.add(product_data)
    session.commit()
    session.close()
