from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, MetaData, ForeignKey
from sqlalchemy.orm import relationship


Base = declarative_base()
metadata = MetaData()

# Don't forget to add password attribut on users table


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    firstname = Column(String)
    addresses = relationship('Address', backref='user')

    def __init__(self, name, firstname, addresses=[]):
        self.name = name
        self.firstname = firstname
        self.addresses = addresses

    def __repr__(self):
        return "<User(name='%s', firstname'%s', email='%s')>" % (
            self.name, self.firstname)


class Address(Base):
    __tablename__ = 'address'
    id = Column(Integer, primary_key=True)
    email = Column(String)
    user_id = Column(Integer, ForeignKey('user.id'))

    def __repr__(self):
        return "<Address(email='%s')>" % (
            self.email)


if __name__ == '__main__':
    engine = create_engine('postgresql://localhost/ingredients_db')

    print("--- Construct all tables for the database (here just one table) ---")
    Base.metadata.create_all(engine)

    print("--- Create three new contacts and push its into the database ---")
    Session = sessionmaker(bind=engine)
    session = Session()
    a = Address(email='fred@aol.com')
    session.add(User(name='wendy', firstname='Williams'))
    # p.addresses.append(a)
    session.add(a)
    # session.add(p)
    session.commit()
