from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker
import getpass

DB_DEFAULTS = {
    "host": "localhost",
    "port": 25432,
    "database": "gis",
    "userid": "docker",
}

DB_CONNECTION = None


def connect_to_db(conn_string):
    try:
        engine = create_engine(conn_string)
        return {
            "engine": engine,
            "connection": engine.connect()
        }
    except Exception as e:
        print(f"{e}")
        quit(1)


def get_tables(engine):
    metadata = MetaData()
    metadata.reflect(bind=engine)
    inspector = inspect(engine)

    for table in inspector.get_table_names():
        print(f"{table}")
        for column in inspector.get_columns(table):
            print(f"... {column}")
        for k, v in inspector.get_pk_constraint(table).items():
            print(f"{k}: {v}")
        print(f"\n{'-' * 20}")


def make_tables_and_return_session(engine):
    # A declarative base class is created with the declarative_base() function.
    Base = declarative_base()

    # The user-defined Car class is mapped to the Cars table. The class inherits from the declarative base
    # class.
    class Car(Base):
        __tablename__ = "Cars"

        Id = Column(Integer, primary_key=True)
        Name = Column(String)
        Price = Column(Integer)

    # The declarative Base is bound to the database engine.
    Base.metadata.bind = engine

    # The create_all() method creates all configured tables; in our case, there is only one table.
    Base.metadata.create_all()

    # A session object is created.
    Session = sessionmaker(bind=engine)

    session = Session()

    session.add_all(
        [Car(Id=1, Name='Audi', Price=52642),
         Car(Id=2, Name='Mercedes', Price=57127),
         Car(Id=3, Name='Skoda', Price=9000),
         Car(Id=4, Name='Volvo', Price=29000),
         Car(Id=5, Name='Bentley', Price=350000),
         Car(Id=6, Name='Citroen', Price=21000),
         Car(Id=7, Name='Hummer', Price=41400),
         Car(Id=8, Name='Volkswagen', Price=21600)])
    session.commit()


def query_data(session, table):
    try:
        return session.query(Base.metadata.tables[table]).all()


def main():
    try:
        host = input(f"Host: (ENTER for 'localhost')") or DB_DEFAULTS["host"]
        port = input(f"Port: (ENTER for 25432)") or f'{DB_DEFAULTS["port"]}'
        database = input(f"Database: (ENTER for 'gis')") or DB_DEFAULTS["database"]
        uid = input(f"UserId: (ENTER for 'docker')") or DB_DEFAULTS["userid"]
        pwd = getpass.getpass()
        DB_CONNECTION = f"postgresql://{uid}:{pwd}@{host}:{port}/{database}"

        # connection = connect_to_db(DB_CONNECTION)["connection"]
        engine = connect_to_db(DB_CONNECTION)["engine"]
        if engine:
            session = make_tables_and_return_session(engine=engine) or None
        if session:
            add_data_to_table(session=session)



    except Exception as e:
        print(f"{e}")
        quit(1)


if __name__ == "__main__":
    main()
