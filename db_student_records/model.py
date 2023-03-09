from sqlalchemy import Column, DateTime, String, Integer, ForeignKey, func
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base

import connection as conn

# A declarative base class is created with the declarative_base() function.
Base = declarative_base()
# The declarative Base is bound to the database engine.
# Base.metadata.bind = conn.engine


# The user-defined classes are mapped to the appropriate tables. The class inherits from the declarative base class.
class Student(Base):
    __tablename__ = "student"
    student_no = Column(String(8), primary_key=True)
    first_name = Column(String(50))
    last_name = Column(String(50))
    phone = Column(String(50))
    modules = relationship(
        "Module",
        secondary="student_module"
    )

    @property
    def name(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def email(self):
        return f"{self.first_name}.{self.last_name}@tudublin.ie"

    def __str__(self):
        return f"{self.student_no}: {self.name}"


class Module(Base):
    __tablename__ = "module"
    mod_code = Column(String(8), primary_key=True)
    name = Column(String(50))
    location = Column(String(50))
    students = relationship(
        "Student",
        secondary="student_module"
    )

    def __str__(self):
        return f"{self.mod_code}: {self.name}"


class StudentModule(Base):
    __tablename__ = "student_module"
    student_no = Column(String(8), ForeignKey("student.student_no"), primary_key=True)
    mod_code = Column(String(8), ForeignKey("module.mod_code"), primary_key=True)
    grade = Column(Integer, default=0)
    student = relationship(Student, backref=backref("student_assoc"))
    module = relationship(Module, backref=backref("module_assoc"))


# Create all tables in the engine. This is equivalent to "Create Table" statements in raw SQL.
# Base.metadata.drop_all(conn.engine)
Base.metadata.create_all(conn.engine)
