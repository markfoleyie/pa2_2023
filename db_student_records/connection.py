from sqlalchemy import create_engine
import getpass

# PostgreSQL example
DB_DEFAULTS = {
    "protocol": "postgresql",
    "host": "localhost",
    "port": 25432,
    "database": "pa2",
    "userid": "docker",
}

# # MySQL sample -> mysql+pymysql://root:password@127.0.0.1/logdb
# DB_DEFAULTS = {
#     "protocol": "mysql+pymysql",
#     "host": "localhost",
#     "port": 23306,
#     "database": "pa2",
#     "userid": "root",
# }


protocol = input(f"Protocol: (ENTER for 'postgresql')") or DB_DEFAULTS["protocol"]
host = input(f"Host: (ENTER for 'localhost')") or DB_DEFAULTS["host"]
port = input(f"Port: (ENTER for 25432)") or f'{DB_DEFAULTS["port"]}'
database = input(f"Database: (ENTER for 'pa2')") or DB_DEFAULTS["database"]
uid = input(f"UserId: (ENTER for 'docker')") or DB_DEFAULTS["userid"]
pwd = getpass.getpass()
db_connection = f"{protocol}://{uid}:{pwd}@{host}:{port}/{database}"

try:
    engine = create_engine(db_connection)
    # connection = engine.connect()
except Exception as e:
    print(f"{e}")
    quit(1)