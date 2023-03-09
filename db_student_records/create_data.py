from sqlalchemy.orm import sessionmaker
import connection as conn
from model import Student, Module, StudentModule, Base

# Bind the engine to the metadata of the Base class so that the declaratives can be accessed through a DBSession
# instance
# Base.metadata.bind = conn.engine

Session = sessionmaker(bind=conn.engine)
# A Session() instance establishes all conversations with the database and represents a "staging zone" for all the
# objects loaded into the database session object. Any change made against the objects in the session won't be
# persisted into the database until you call session.commit(). If you're not happy about the changes, you can revert
# all of them back to the last commit by calling session.rollback()
session = Session()

students = [
    {"student_no": "c1111", "first_name": "alan", "last_name": "anderson", "phone": "+353871119999", },
    {"student_no": "c2222", "first_name": "brian", "last_name": "buckley", "phone": "+353871118888", },
    {"student_no": "c3333", "first_name": "charlie", "last_name": "clarke", "phone": "+353871117777", },
    {"student_no": "c4444", "first_name": "doreen", "last_name": "delany", "phone": "+353871116666", },
    {"student_no": "c5555", "first_name": "elaine", "last_name": "egan", "phone": "+353871115555", },
    {"student_no": "c6666", "first_name": "frank", "last_name": "farrell", "phone": "+353871114444", },
    {"student_no": "c7777", "first_name": "gerry", "last_name": "grimes", "phone": "+353871113333", },
]

modules = [
    {"mod_code": "cmpu1001", "name": "programming in python", "location": "central quad", },
    {"mod_code": "cmpu1002", "name": "management 101", "location": "east quad", },
    {"mod_code": "cmpu1003", "name": "computing fundamentals", "location": "west quad", },
    {"mod_code": "cmpu1004", "name": "programming in java", "location": "central quad", },
    {"mod_code": "cmpu1005", "name": "engineering 101", "location": "central quad", },
    {"mod_code": "cmpu1006", "name": "web development 1", "location": "east quad", },
]

student_modules = [
    {"student_no": "c1111", "mod_code": "cmpu1001",},
    {"student_no": "c1111", "mod_code": "cmpu1002", },
    {"student_no": "c1111", "mod_code": "cmpu1003", },
    {"student_no": "c2222", "mod_code": "cmpu1001", },
    {"student_no": "c2222", "mod_code": "cmpu1002", },
    {"student_no": "c3333", "mod_code": "cmpu1001", },
    {"student_no": "c4444", "mod_code": "cmpu1001", },
    {"student_no": "c4444", "mod_code": "cmpu1002", },
    {"student_no": "c4444", "mod_code": "cmpu1003", },
    {"student_no": "c4444", "mod_code": "cmpu1004", },
    {"student_no": "c4444", "mod_code": "cmpu1005", },
]


for student in students:
    try:
        new_student = Student(**student)
        session.add(new_student)
        session.commit()
    except:
        pass
for module in modules:
    try:
        new_module = Module(**module)
        session.add(new_module)
        session.commit()
    except:
        pass

for entry in student_modules:
    try:
        new_entry = StudentModule(**entry)
        session.add(new_entry)
        session.commit()
    except:
        pass

