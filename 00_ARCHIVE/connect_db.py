from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, MetaData


Base = declarative_base()
metadata = MetaData()

# Don't forget to add password attribut on users table


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    firstname = Column(String)
    addresses = relationship('Address', backref='user')

    def __repr__(self):
        return "<User(name='%s', firstname'%s', email='%s')>" % (
            self.name, self.firstname)


class Address(Base):
    id = Column(Integer, primary_key=True)
    email = Column(String)
    user_id = Column(Integer, ForeignKey('user.id'))


if __name__ == '__main__':
    engine = create_engine('postgresql://localhost/ingredients_db')

    print("--- Construct all tables for the database (here just one table) ---")
    Base.metadata.create_all(engine)

    print("--- Create three new contacts and push its into the database ---")
    Session = sessionmaker(bind=engine)
    session = Session()
    session.add_all([
        User(name='wendy', firstname='Williams', email='wendy@aol.com'),
        User(name='mary', firstname='Contrary', email='mary@aol.com'),
        User(name='fred', firstname='Flinstone', email='fred@aol.com')])
    session.new
    session.commit()
