import requests
from sqlalchemy import create_engine, and_
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func


Base = declarative_base()
metadata = MetaData()

Product_category = Table('product_category', Base.metadata,
                         Column('id_product', Integer,
                                ForeignKey('product.id')),
                         Column('id_category', Integer,
                                ForeignKey('category.id'))
                         )


class Product(Base):
    __tablename__ = 'product'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    nutriscore = Column(String)
    nova = Column(String)
    categories = relationship(
        "Category",
        secondary=Product_category, back_populates="products")
    brands = relationship("Brand", back_populates="product")

    def __repr__(self):
        return "<Product(name='%s', nutriscore='%s', nova='%s')>" % (self.name,
                                                                     self.nutriscore,
                                                                     self.nova)


class Category(Base):
    __tablename__ = 'category'

    id = Column(Integer, primary_key=True)
    name = Column(String)

    products = relationship(
        "Product",
        secondary=Product_category,
        back_populates="categories")

    def __repr__(self):
        return "<Category(name='%s')>" % (self.name)


class Brand(Base):
    __tablename__ = 'brand'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    label = Column(String)
    product_id = Column(Integer, ForeignKey('product.id'))
    products = relationship("Product", back_populates="brand")

    def __repr__(self):
        return "<Brand(name='%s', label='%s')>" % (self.name, self.label)


print("--- Construct all tables for the database (here just one table) ---")
global Session
engine = create_engine('postgresql://localhost/ingredients_db')
Session = sessionmaker(bind=engine)
Base.metadata.create_all(engine)


def move_duplicate():
    session = Session()
    # helper subquery: find first row (by primary key) for each unique date
    subq = (
        session.query(Brand.name, func.min(Brand.id).label("min_id"))
        .group_by(Brand.name)
    ) .subquery('name_min_id')

    # query to find all duplicates
    q_duplicates = (
        session
        .query(Brand)
        .join(subq, and_(
            Brand.name == subq.c.name,
            Brand.id != subq.c.min_id)
        )
    )

    for x in q_duplicates:
        print("Will delete %s" % x)
        session.delete(x)
    session.commit()


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
        # session.add(Category(name=category))
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
        for product_name in results_2["products"]:
            if product_name.get("product_name") != "":
                #marque = Brand(name=product_name.get("brands"))
                produit = Product(name=product_name.get("product_name"),
                                  nutriscore=product_name.get(
                    "nutrition_grades"),
                    nova=product_name.get("nova_groups_tags"))
                # marque.products.append(produit)
                # produit.brand.append(marque)
                # session.add(marque)
                session.add(produit)

            # query = session.query(Brand.id).filter(
            #    Brand.name == product_name.get("brands"))
            # for row in query:
            #    print(row._asdict())

    session.commit()
    session.close()


add_data()
move_duplicate()
