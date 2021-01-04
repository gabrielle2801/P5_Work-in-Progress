from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey
from sqlalchemy.orm import relationship


Base = declarative_base()
metadata = MetaData()

product_category = Table('product_category', Base.metadata,
                         Column('product_id', Integer,
                                ForeignKey('product.id')),
                         Column('category_id', Integer,
                                ForeignKey('category.id'))
                         )

product_store = Table('product_store', Base.metadata,
                      Column('product_id', Integer, ForeignKey('product.id')),
                      Column('store_id', Integer,
                             ForeignKey('store.id'))
                      )
product_subtitute = Table('product_subtituteu', Base.metadata,
                          Column('product_id', Integer,
                                 ForeignKey('product.id')),
                          Column('subtitute_id', Integer,
                                 ForeignKey('subtitute.id'))
                          )


class Product(Base):
    __tablename__ = 'product'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    nutriscore = Column(String)
    nova = Column(Integer)
    url = Column(String)
    barcode = Column(String)
    description = Column(String)
    brand_id = Column(Integer, ForeignKey(
        'brand.id', onupdate="CASCADE", ondelete="CASCADE"), nullable=False)
    brand = relationship("Brand", backref="brands", lazy=True)

    categories = relationship(
        "Category",
        secondary=product_category, backref="products")
    stores = relationship(
        "Store",
        secondary=product_store,
        backref="products")
    subtitutes = relationship(
        "Subtitute",
        secondary=product_subtitute,
        backref="products")

    def __repr__(self):
        return "<Product(name='%s', nutriscore='%s', nova='%s',\
                                                     url='%s', description='%s',barcode='%s')>"\
            % (self.name, self.nutriscore, self.nova, self.url, self.description, self.barcode)


class Subtitute(Base):
    __tablename__ = 'subtitute'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    nutriscore = Column(String)
    description = Column(String)
    store = Column(String)
    url = Column(String)

    def __repr__(self):
        return "<Product(name='%s', nutriscore='%s',description='%s',\
                                            store='%s',url='%s')>"\
                % (self.name, self.nutriscore, self.description, self.store, self.url)


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


print("--- Construct all tables for the database  ---")
global Session
engine = create_engine('postgresql://localhost/test')
Session = sessionmaker(bind=engine)
Base.metadata.create_all(engine)
