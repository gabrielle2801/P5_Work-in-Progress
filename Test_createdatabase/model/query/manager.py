from off.model.db.models import Product, Category, Store, Substitute, Brand
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy import asc
global Session
engine = create_engine('postgresql://localhost/db_off')
Session = sessionmaker(bind=engine)


class DBManager():
    def __init__(self):
        self.session = Session()

    # import categories on DataBase
    def get_or_create_category(self, category_name):

        category = self.session.query(Category).filter(
            Category.name == category_name).first()
        if not category:
            category = Category(name=category_name)
            self.session.add(category)
        return category

    # import brand on DataBase
    def get_or_create_brand(self, brand_name, label):

        brand = self.session.query(Brand).filter(
            Brand.name == brand_name).first()
        if not brand or brand == "":
            brand = Brand(name=brand_name, label=label)
            self.session.add(brand)
        return brand

    # Research by category
    def get_categories(self):
        return self.session.query(Category).select_from(Category).order_by(
            asc(Category.name)).all()

    def get_products_for_category(self, category_id):
        return self.session.query(Product).select_from(Category)\
            .join(Product.categories).filter(Category.id == category_id).all()

    def get_substitutes(self, product_id, category_id=None):
        product = self.get_products(product_id)
        if not category_id:
            category_id = product.categories[0].id
        result = []

        product_search = self.session.query(Product).\
            select_from(Category).join(Product.categories).\
            filter(Category.id == category_id,
                   Product.nutriscore < product.nutriscore,
                   Product.nova < product.nova).all()
        result.extend(product_search)
        return result

    # get stores for product search by categorie
    def get_stores_for_product(self, product_id):
        stores_list = self.session.query(Store).select_from(Product)\
            .join(Product.stores).filter(Product.id == product_id).all()
        store_result = ""
        for store in stores_list:
            store_result = store.name + ", " + store_result
        return store_result

    def get_products(self, product_id):
        return self.session.query(Product).select_from(Product).filter(
            Product.id == product_id).first()

    # Research product by name
    def search_product(self, product_name):
        return self.session.query(Product).select_from(Product).filter(
            Product.name.like('%' + product_name + '%')).all()

    # List of subtitutes saved
    def create_substitute(self, product_id, substitut_id):
        subtitute = self.session.query(Substitute).filter(
            Substitute.product_id == product_id).first()
        if not subtitute:
            substitute = Substitute(substitute_id=substitut_id,
                                    product_id=product_id)
            self.session.add(substitute)
            print("Le produit et son substitut ont bien été enregistré")
        else:
            print("Le produit a déja été sauvegardé dans la liste")
        self.session.commit()

    def get_research_list(self):
        return self.session.query(Product).select_from(Substitute).filter(
            Product.id == Substitute.product_id).all()

    def get_substitute_saved(self):
        return self.session.query(Substitute).all()
