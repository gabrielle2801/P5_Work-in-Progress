import requests
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, MetaData


Base = declarative_base()
metadata = MetaData()


class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True)
    pdt_name = Column(String)
    category = Column(String)

    def __repr__(self):
        return "<Product(product_name='%s', category='%s')>" % (
            self.pdt_name, self.category)

    print("--- Construct all tables for the database (here just one table) ---")
    global Session
    engine = create_engine('postgresql://localhost/ingredients_db')
    Session = sessionmaker(bind=engine)
    Base.metadata.create_all(engine)

    def add_data():
        session = Session()

        response = requests.get(
            "https://fr.openfoodfacts.org/categories.json")
        results = response.json()
        data_category = results.get('tags')
        category_name = [data.get('name', 'None') for data in data_category]
        popular_cat = category_name[0:10]
        query = {"action": "process",
                 "categories": popular_cat,
                 "sort_by": "unique_scans_n",
                 "page_size": 10,
                 "json": 1}

        response_2 = requests.get(
            "https://fr.openfoodfacts.org/cgi/search.pl?", params=query)
        results_2 = response_2.json()
        # print(results_2.keys())
        # pdts = results_2["products"]
        # print(pdts["product_name"])
        for product_name in results_2["products"]:
            session.add_all([
                Product(pdt_name=product_name.get("product_name"), category=popular_cat.get("categories"))])
        session.commit()
        session.close()

    # setUp()
    add_data()
