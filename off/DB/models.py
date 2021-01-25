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

  def __repr__(self):
    return " %s, nutriscore:%s, nova:%s"\
        % (self.name, self.nutriscore, self.nova)


class Substitute(Base):
  __tablename__ = 'substitute'

  id = Column(Integer, primary_key=True)
  product_id = Column(Integer, ForeignKey('product.id'), unique=True)
  substitute_id = Column(Integer, ForeignKey('product.id'))
  product = relationship(
      'Product', lazy=True, foreign_keys=[product_id])
  substitute = relationship(
      'Product', lazy=True, foreign_keys=[substitute_id])

  def __repr__(self):
    return '<Substitute: {}>'.format(self.id)


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


# print("--- Construct all tables for the database  ---")
global Session
engine = create_engine('postgresql://localhost/db_off')
Session = sessionmaker(bind=engine)
Base.metadata.create_all(engine)
