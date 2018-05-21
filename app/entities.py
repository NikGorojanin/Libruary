import sqlalchemy, datetime, time, requests, re, json
from sqlalchemy.ext.declarative import DeclarativeMeta
from sqlalchemy import Table, Column, Integer, ForeignKey
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
from flask import request, Response, redirect, url_for
from sqlalchemy import Column, Integer, String, DateTime, TIMESTAMP, ForeignKey, text, Float, distinct, or_, not_, func, \
    and_, desc, Enum, Boolean, BigInteger, Sequence, MetaData
from sqlalchemy.pool import NullPool
import enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
import flask_login
from flask_login import UserMixin, login_manager

engine = sqlalchemy.create_engine(
    'postgresql+psycopg2://.../libruary', poolclass=NullPool,
    pool_recycle=3600)
Session = scoped_session(sessionmaker(bind=engine))
ses = Session()
Base = declarative_base(bind=engine)
Base.query = Session.query_property()
metadata = MetaData()


class User(Base, UserMixin):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_name = Column(String(255))
    login = Column(String(255))
    password = Column(String(255))

    @staticmethod
    def get(user_id):
        global ses
        try:
            user = ses.query(User).filter(User.id == user_id).one()
        except Exception as exp:
            print("Error while login: {}".format(exp))
            ses.rollback()
            ses.close()
            return None
        ses.close()
        return user

    @staticmethod
    def get_user_from_login_data(login, password):
        global ses
        try:
            user = ses.query(User).filter(User.login == login,
                                          User.password == password).one()
        except Exception as exp:
            print("Error while login: {}".format(exp))
            ses.rollback()
            ses.close()
            return None
        ses.close()
        return user


association_table = Table('association', Base.metadata,
    Column('book_id', Integer, ForeignKey('books.id')),
    Column('author_id', Integer, ForeignKey('authors.id'))
)


class Book(Base):
    __tablename__ = "books"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(1255))
    authors = relationship("Author", secondary=association_table,
                                     backref="books")


class Author(Base):
    __tablename__ = "authors"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255))
    # books = relationship("Book", secondary=association_table, cascade="save-update, merge, delete")




# class BookAuthor(Base):
#     __tablename__ = "book_autor"
#     book_id = Column(Integer, ForeignKey("books.id"), primary_key=True)
#     author_id = Column(Integer, ForeignKey("authors.id"), primary_key=True)
