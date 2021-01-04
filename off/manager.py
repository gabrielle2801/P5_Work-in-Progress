from models import Product, Category, Store
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

global Session
engine = create_engine('postgresql://localhost/test')
Session = sessionmaker(bind=engine)


class Productbycategory():
    def __init__(self):
        self.session = Session()

    def get_category(self):
        return self.session.query(Category.name).select_from(Category).all()

    def get_product(self, category):
        return self.session.query(Product).select_from(Category)\
            .join(Product.categories).filter(Category.name == category.name).all()

    def get_subtitute(self, product, category):
        return self.session.query(Product).select_from(Category)\
            .join(Product.categories).filter(Category.name == category,
                                             Product.nutriscore < product.nutriscore).all()

    def get_store(self, product):
        return self.session.query(Store).select_from(Product)\
            .join(Product.stores).filter(Product.name == product.name).all()
