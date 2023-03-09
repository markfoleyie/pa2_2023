import sqlalchemy
import getpass
import tkinter as tk
from tkinter import ttk

DB_DEFAULTS = {
    "host": "localhost",
    "port": 25432,
    "database": "pa2",
    "userid": "docker",
}


class LoginPanel(tk.Tk):
    def __init__(self, db_defaults):
        super().__init__()

        self.protocol("WM_DELETE_WINDOW", self.catch_destroy)

        self.title(f"Database Login")
        self.frame1 = ttk.Frame(self)
        self.frame1.grid()

        padding = {
            "padx": 5,
            "pady": 5,
            "ipadx": 5,
            "ipady": 5,
        }

        self.values = {}
        self.objects = []
        for k, v in db_defaults.items():
            self.values[k] = tk.StringVar()
            self.values[k].set(v)

        row = 0
        for k in self.values:
            self.objects.append(
                ttk.Label(self.frame1, text=f"{k.title()}: ").grid(row=row, column=0, sticky="e", **padding))
            self.objects.append(
                ttk.Entry(self.frame1, textvariable=self.values[k]).grid(row=row, column=1, sticky="w", **padding))
            row += 1

        self.values["password"] = tk.StringVar()
        self.objects.append(ttk.Label(self.frame1, text=f"Password: ").grid(row=row, column=0, sticky="e", **padding))
        self.objects.append(
            ttk.Entry(self.frame1, textvariable=self.values["password"], show="*").grid(row=row, column=1, sticky="w",
                                                                                        **padding))
        row += 1

        self.objects.append(
            ttk.Button(self.frame1, text="OK", width=8, command=self.ok_pressed).grid(row=row, column=0, sticky="e",
                                                                                      **padding))
        self.objects.append(
            ttk.Button(self.frame1, text="Cancel", width=8, command=self.cancel_pressed).grid(row=row, column=1,
                                                                                              sticky="w", **padding))

    def ok_pressed(self):
        globals()["DB_CONNECTION"] = f"postgresql://{self.values['userid'].get()}:" \
                                     f"{self.values['password'].get()}@" \
                                     f"{self.values['host'].get()}:" \
                                     f"{self.values['port'].get()}/" \
                                     f"{self.values['database'].get()}"
        self.destroy()

    def cancel_pressed(self):
        self.catch_destroy()

    def catch_destroy(self):
        globals()["DB_CONNECTION"] = None
        self.destroy()


def connect_to_db(conn_string):
    try:
        engine = sqlalchemy.create_engine(conn_string)
        return {
            "engine": engine,
            "connection": engine.connect()
        }
    except Exception as e:
        print(f"{e}")
        quit(1)


def get_tables(engine):
    metadata = sqlalchemy.MetaData()
    metadata.reflect(bind=engine)
    inspector = sqlalchemy.inspect(engine)

    for table in inspector.get_table_names():
        print(f"{table}")
        for column in inspector.get_columns(table):
            print(f"... {column}")
        for k, v in inspector.get_pk_constraint(table).items():
            print(f"{k}: {v}")
        print(f"\n{'-' * 20}")

    print(f"{inspector.get_schema_names()}")


def main():
    try:
        # login = LoginPanel(DB_DEFAULTS)
        # login.mainloop()
        host = input(f"Host: (ENTER for 'localhost')") or DB_DEFAULTS["host"]
        port = input(f"Port: (ENTER for 25432)") or f'{DB_DEFAULTS["port"]}'
        database = input(f"Database: (ENTER for 'pa2')") or DB_DEFAULTS["database"]
        uid = input(f"UserId: (ENTER for 'docker')") or DB_DEFAULTS["userid"]
        pwd = getpass.getpass()
        globals()["DB_CONNECTION"] = f"postgresql://{uid}:{pwd}@{host}:{port}/{database}"

        if globals()["DB_CONNECTION"]:
            connection = connect_to_db(globals()["DB_CONNECTION"])["connection"]
            engine = connect_to_db(globals()["DB_CONNECTION"])["engine"]

            get_tables(engine)

    except Exception as e:
        print(f"{e}")
        quit(1)


if __name__ == "__main__":
    main()
