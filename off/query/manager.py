from DB.models import Product, Category, Store, Subtitute, Brand
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

global Session
engine = create_engine('postgresql://localhost/test')
Session = sessionmaker(bind=engine)


class DBManager():
    def __init__(self):
        self.session = Session()

    def get_categories(self):
        return self.session.query(Category).select_from(Category).all()

    def get_or_create_category(self, category_name):

        category = self.session.query(Category).filter(
            Category.name == category_name).first()
        if not category:
            category = Category(name=category_name)
            self.session.add(category)
        return category

    def get_or_create_brand(self, brand_name, label):

        brand = self.session.query(Brand).filter(
            Brand.name == brand_name).first()
        if not brand:
            brand = Brand(name=brand_name, label=label)
            self.session.add(brand)
        return brand

    def get_products_for_category(self, category_id):
        return self.session.query(Product).select_from(Category)\
            .join(Product.categories).filter(Category.id == category_id).all()

    def get_subtitutes(self, product_id, category_id):
        product = self.get_products(product_id)
        return self.session.query(Product).select_from(Category)\
            .join(Product.categories).filter(Category.id == category_id,
                                             Product.nutriscore < product.nutriscore).all()

    def get_stores_for_product(self, product_id):
        return self.session.query(Store).select_from(Product)\
            .join(Product.stores).filter(Product.id == product_id).all()

    def get_products(self, product_id):
        return self.session.query(Product).select_from(Product).filter(Product.id == product_id).first()

    def get_product_by_name(self, product_name):
        return self.session.query(Product).select_from(Product).filter(Product.name == product_name).first()

    def create_subtitute(self, product_id, subtitut_id):
        subtitut = Subtitute(subtitute_id=subtitut_id,
                             product_id=product_id)
        self.session.add(subtitut)
        self.session.commit()

    def get_research_list(self):
        return self.session.query(Product).select_from(Subtitute).join(Subtitute.product).filter(
            Product.id == Subtitute.product_id)

    def get_subtitute_saved(self):
        return self.session.query(Product).select_from(Subtitute).filter(
            Product.id == Subtitute.subtitute_id).all()
