from sqlalchemy import create_engine, MetaData, inspect, Table
from sqlalchemy.sql import text, select

uid = "docker"
pwd = "docker"
host = "localhost"
port = 25432
database = "pa2"
conn_string = f"postgresql://{uid}:{pwd}@{host}:{port}/{database}"

eng = create_engine(conn_string)

# PostgreSQL version
con = eng.connect()
rs = con.execute(text("SELECT VERSION()"))
print(rs.fetchone())

con.close()

# Creating a database table
data = ({"id": 1, "name": "Audi", "price": 52642},
        {"id": 2, "name": "Mercedes", "price": 57127},
        {"id": 3, "name": "Skoda", "price": 9000},
        {"id": 4, "name": "Volvo", "price": 29000},
        {"id": 5, "name": "Bentley", "price": 350000},
        {"id": 6, "name": "Citroen", "price": 21000},
        {"id": 7, "name": "Hummer", "price": 41400},
        {"id": 8, "name": "Volkswagen", "price": 21600}
        )

# Create table
with eng.connect() as con:
    con.execute(text("DROP TABLE IF EXISTS cars"))
    con.execute(text("CREATE TABLE cars(id INTEGER PRIMARY KEY, name TEXT, price INTEGER)"))
    con.commit()

# Insert data
with eng.connect() as con:
    for line in data:
        qry = text("INSERT INTO cars(id, name, price) VALUES(:id, :name, :price)")
        con.execute(qry, line)
    con.commit()

# Query table
with eng.connect() as con:
    for item in con.execute(text("SELECT * FROM cars")).fetchall():
        print(item)

# Print metadata
meta = MetaData()
meta.reflect(bind=eng)
for table in meta.tables:
    print(table)

insp = inspect(eng)
print(insp.get_table_names())
print(insp.get_columns("cars"))
# print(insp.get_primary_keys("cars"))
print(insp.get_schema_names())

with eng.connect() as con:
    cars = Table('cars', meta, autoload=True)
    stm = select(cars)
    rs = con.execute(stm)
    print(rs.fetchall())