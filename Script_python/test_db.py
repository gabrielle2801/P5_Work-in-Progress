import requests
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, MetaData, ForeignKey
from sqlalchemy.orm import relationship


Base = declarative_base()
metadata = MetaData()


class Product_Category(Base):
    __tablename__ = 'product_category'
    product_id = Column(Integer, ForeignKey('product.id'), primary_key=True)
    category_id = Column(Integer, ForeignKey(
        'category.id'), primary_key=True)


class Product(Base):
    __tablename__ = 'product'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    nutriscore = Column(String)
    nova = Column(String)
    categories = relationship(
        "Category",
        secondary="Product_Category", backref="products", lazy=True)
    brand_id = Column(Integer, ForeignKey('brand.id'))
    brand = relationship("Brand", backref="brands", lazy=True)

    def __repr__(self):
        return "<Product(name='%s', nutriscore='%s', nova='%s')>"\
            % (self.name, self.nutriscore, self.nova)


class Category(Base):
    __tablename__ = 'category'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    products = relationship(
        "Product",
        secondary="Product_Category", backref="categories", lazy=True)

    def __repr__(self):
        return "<Category(name='%s')>" % (self.name)


class Brand(Base):
    __tablename__ = 'brand'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    label = Column(String)
    # products = relationship("Product", back_populates="brand")

    def __repr__(self):
        return "<Brand(name='%s', label='%s')>" % (self.name, self.label)


print("--- Construct all tables for the database (here just one table) ---")
global Session
engine = create_engine('postgresql://localhost/test')
Session = sessionmaker(bind=engine)
Base.metadata.create_all(engine)

# Function does not work to remove duplicates ...


def get_brand(name):
    session = Session()
    return session.query(Brand).filter(Brand.name == 'name')


def add_data():
    session = Session()
    response = requests.get(
        "https://fr.openfoodfacts.org/categories.json?sort_by=products")
    results = response.json()
    data_category = results.get('tags')
    category_name = [data.get('name', 'None') for data in data_category]
    popular_cat = category_name[0:10]

    for category in popular_cat:
        print(category)
        session.add(Category(name=category))
        query = {
            "action": "process",
            "tagtype_0": "categories",
            "tag_contains_0": "contains",
            "tag_0": category,
            "sort_by": "unique_scans_n",
            "page_size": 10,
            "json": 1}

        response_2 = requests.get(
            "https://fr.openfoodfacts.org/cgi/search.pl?", params=query)
        results_2 = response_2.json()
        for item in results_2["products"]:
            if item.get("product_name") != "":
                # b = get_brand(item.get("brands"))
                b = session.query(Brand).filter(
                    Brand.name == item.get("brands")).first()
                print(b)
                if not b:
                    brand = Brand(name=item.get("brands"),
                                  label=item.get("label"))
                    session.add(brand)
                    b = session.query(Brand).filter(
                        Brand.name == item.get("brands")).first()
                session.add(Product(name=item.get("product_name"),
                                    nutriscore=item.get(
                    "nutrition_grades"),
                    nova=item.get("nova_groups_tags"),
                    brand=b))
            p = session.query(Product.filter(
                Product.name == item.get("products").first()))
            c = session.query(Category.filter(
                Category.name == item.get("category").first()))
            session.add(Product_Category(product_id=p,
                                         category_id=c))

    session.commit()
    session.close()


if __name__ == "__main__":
    add_data()
