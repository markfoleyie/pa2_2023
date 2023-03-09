from sqlalchemy.orm import sessionmaker
import connection as conn
from model import Student, Module, StudentModule, Base

# Bind the engine to the metadata of the Base class so that the declaratives can be accessed through a DBSession
# instance
# Base.metadata.bind = conn.engine

DBSession = sessionmaker(bind=conn.engine)
# A DBSession() instance establishes all conversations with the database and represents a "staging zone" for all the
# objects loaded into the database session object. Any change made against the objects in the session won't be
# persisted into the database until you call session.commit(). If you're not happy about the changes, you can revert
# all of them back to the last commit by calling session.rollback()
session = DBSession()

students = session.query(Student).all()

print(f"{'ID':<6}|{'Name':<15}|{'email':<20}")
print(f"{'-'*6}+{'-'*15}+{'-'*20}")

for student in students:
    print(f"{student.student_no:<6}|{student.name:<15}|{student.email:<20}")

print(f"{'='*50}")
modules = session.query(Module).all()

print(f"{'Code':<9}|{'Name':<15}")
print(f"{'-'*9}+{'-'*15}")

for module in modules:
    print(f"{module.mod_code:<9}|{module.name:<15}")