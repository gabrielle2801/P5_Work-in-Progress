from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey
from sqlalchemy.orm import relationship


Base = declarative_base()
metadata = MetaData()
Product_category = Table('product_category', Base.metadata,
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
    barcode = Column(String)
    brand_id = Column(Integer, ForeignKey(
        'brand.id', onupdate="CASCADE", ondelete="CASCADE"), nullable=False)
    brand = relationship("Brand", backref="brands", lazy=True)

    categories = relationship(
        "Category",
        secondary=Product_category, backref="product")
    stores = relationship(
        "Store",
        secondary=product_store,
        backref="products")

    def __repr__(self):
        return "<Product(name='%s', nutriscore='%s', nova='%s',\
                                                     url='%s', barcode='%s')>"\
            % (self.name, self.nutriscore, self.nova, self.url, self.barcode)


class Brand(Base):
    __tablename__ = 'brand'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    label = Column(String)

    def __repr__(self):
        return "<Brand(name='%s', label='%s')>" % (self.name,
                                                   self.label)


class Category(Base):
    __tablename__ = 'category'

    id = Column(Integer, primary_key=True)
    name = Column(String)

    def __repr__(self):
        return "<Category(name='%s')>" % (self.name)


class Store(Base):
    __tablename__ = 'store'

    id = Column(Integer, primary_key=True)
    name = Column(String)

    def __repr__(self):
        return "<Store(name='%s'))>" % (self.name)


print("--- Construct all tables for the database (here just one table) ---")
global Session
engine = create_engine('postgresql://localhost/ingredients_db')
Session = sessionmaker(bind=engine)
Base.metadata.create_all(engine)
