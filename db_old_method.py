"""
In this design, we have two tables person and address and
address.person_id is a foreign key to the person table.
"""
import sqlite3


def create_db():
    conn = sqlite3.connect('example2.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE person (id INTEGER PRIMARY KEY ASC, name varchar(250) NOT NULL)''')
    c.execute('''
    CREATE TABLE address (id INTEGER PRIMARY KEY ASC, street_name varchar(250), street_number varchar(250),
    post_code varchar(250) NOT NULL, person_id INTEGER NOT NULL,
    FOREIGN KEY(person_id) REFERENCES person(id))
    ''')
    c.execute('''INSERT INTO person VALUES(1, 'pythoncentral')''')
    c.execute('''INSERT INTO address VALUES(1, 'python road', '1', '00000', 1)''')
    conn.commit()
    conn.close()


def query_db():
    """
    Now we can query the database example.db to fetch the records.
    """
    conn = sqlite3.connect('example2.db')
    c = conn.cursor()
    c.execute('SELECT * FROM person')
    print(c.fetchall())
    c.execute('SELECT * FROM address')
    print(c.fetchall())
    conn.close()


def main():
    create_db()
    query_db()


if __name__ == "__main__":
    main()
