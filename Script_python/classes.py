from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey
from sqlalchemy.orm import relationship


Base = declarative_base()
metadata = MetaData()

product_category = Table('product_category', Base.metadata,
                         Column('id_product', Integer,
                                ForeignKey('product.id')),
                         Column('id_category', Integer,
                                ForeignKey('category.id'))
                         )
product_store = Table('product_store', Base.metadata,
                      Column('id_product', Integer, ForeignKey('product.id')),
                      Column('id_store', Integer,
                             ForeignKey('store.id'))
                      )


class Product(Base):
    __tablename__ = 'product'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    nutriscore = Column(String)
    nova = Column(String)
    url = Column(String)
    barcode = Column(Integer)
    brand_id = Column(Integer, ForeignKey=('brands.id'))
    brands = relationship("Brand", back_populates="product")

    categories = relationship(
        "Category",
        secondary=product_category, back_populates="product")
    stores = relationship(
        "Store",
        secondary=product_store,
        back_populates="products")

    def __init__(self, name, nutriscore, nova, url, barcode):
        self.name = name
        self.nutriscore = nutriscore
        self.nova = nova
        self.url = url
        self.barcode = barcode

    def __repr__(self):
        return "<Product(name='%s', nutriscore='%s', nova='%s')>" % (self.name,
                                                                     self.nutriscore,
                                                                     self.nova,
                                                                     self.url,
                                                                     self.barcode)


class Brand(Base):
    __tablename__ = 'brand'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    label = Column(String)
    products = relationship("Product", back_populates="brand")

    def __init__(self, name, label):
        self.name = name
        self.label = label

    def __repr__(self):
        return "<Brand(name='%s', label='%s')>" % (self.name,
                                                   self.label)


class Category(Base):
    __tablename__ = 'category'

    id = Column(Integer, primary_key=True)
    name = Column(String)

    products = relationship(
        "Product",
        secondary=product_category,
        back_populates="categories")

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return "<Category(name='%s')>" % (self.name)


class Store(Base):
    __tablename__ = 'store'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    products = relationship(
        "Product",
        secondary=product_store,
        back_populates="store")

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return "<Store(name='%s'))>" % (self.name)
