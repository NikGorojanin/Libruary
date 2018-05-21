from app.entities import *
from flask import jsonify
import json
from datetime import datetime


def add_book(book_name, authors_ids):
    global ses
    try:
        # same_books = ses.query(Book).filter(Book.name == book_name).all()
        # if same_books is not None:
        #     for same_book in same_books:
        #         is_same_book = True
        #         for author in same_book.authors:
        #             if author.id not in authors_ids:
        #                 is_same_book = False
        #                 break
        #         if is_same_book:
        #             return {'status': 'failed', 'reason': 'Книга уже существует!'}

        new_book = Book(name=book_name)
        if len(authors_ids) > 0:
            authors = ses.query(Author).filter(Author.id.in_(authors_ids)).all()
            print(authors)
            for author in authors:
                new_book.authors.append(author)

        ses.add(new_book)
        ses.commit()
        ses.close()
        return {'status': 'success'}
    except Exception as exp:
        print(exp)
        ses.rollback()
        ses.close()
        return {'status': 'failed', 'reason': str(exp)}


def add_author(author_name, books_ids):
    global ses
    try:
        # same_authors = ses.query(Author).filter(Author.name == author_name).all()
        # if same_authors is not None:
        #     for same_author in same_authors:
        #         is_same_author = True
        #         for book in same_author.books:
        #             if book.id not in books_ids:
        #                 is_same_author = False
        #                 break
        #         if is_same_author:
        #             return {'status': 'failed', 'reason': 'Автор уже существует!'}

        new_author = Author(name=author_name)
        if len(books_ids) > 0:
            books = ses.query(Book).filter(Book.id.in_(books_ids)).all()
            for book in books:
                new_author.books.append(book)

        ses.add(new_author)
        ses.commit()
        ses.close()
        return {'status': 'success'}
    except Exception as exp:
        print(exp)
        ses.rollback()
        ses.close()
        return {'status': 'failed', 'reason': str(exp)}


def load_books():
    global ses
    # try:
    # ses.close()
    books = ses.query(Book).all()
    books_list = [{'id': book.id, 'name': book.name} for book in books]
    # ses.close()
    return {'status': 'success', 'data': books_list}
# except Exception as exp:
#     ses.rollback()
#     ses.close()
    return {'status': 'failed', 'reason': "lalala1"}


def load_authors():
    global ses
    # try:
    authors = ses.query(Author).all()
    authors_list = [{'id': author.id, 'name': author.name} for author in authors]
    print(authors_list)
    # ses.close()
    return {'status': 'success', 'data': authors_list}
    # except Exception as exp:
    #     print(exp)
    #     ses.rollback()
    #     ses.close()
    #     return {'status': 'failed', 'reason': str(exp)}


def load_data_for_table():
    global ses
    # try:
    books = ses.query(Book).all()
    print(books)
    table_data = []
    for book in books:
        author_names = [_.name for _ in book.authors]
        authors = ", ".join(author_names)
        table_data.append({'book': book.name, 'author': authors})
    # ses.close()
    return {'status': 'success', 'data': table_data}
    # except Exception as exp:
    #     ses.rollback()
    #     ses.close()
    #     return {'status': 'failed', 'reason': str(exp)}


def find_books(user_query, by_whom):
    global ses
    try:
        table_data = []
        if by_whom == "both":
            books = ses.query(Book).join(Author, Book.authors).filter(or_(Author.name.like("%{}%".format(user_query)),
                                                                       Book.name.like("%{}%".format(user_query)))).all()
        elif by_whom == "book":
            books = ses.query(Book).join(Author, Book.authors)\
                                   .filter(or_(Book.name.like("%{}%".format(user_query)))).all()
        else:
            books = ses.query(Book).join(Author, Book.authors)\
                                   .filter(or_(Author.name.like("%{}%".format(user_query)))).all()

        for book in books:
            authors = ", ".join(book.authors)
            table_data.append({'book': book.name, 'author': authors})

        return {'status': 'success', 'data': table_data}
        # if by_whom == "book":
        #     books = ses.query(Book).filter(Book.name.like("%{}%".format(user_query))).all()
        #     table_data = []
        #     for book in books:
        #         authors = ", ".join(book.authors)
        #         table_data.append({'book': book.name, 'author': authors})
        # else:
        #     books = ses.query(Book).join(Author, Book.authors).filter(Author.name.like("%{}%".format(user_query))).all()
        #     table_data = []
        #     for book in books:
        #         authors = ", ".join(book.authors)
        #         table_data.append({'book': book.name, 'author': authors})
    except Exception as exp:
        ses.rollback()
        ses.close()
        return {'status': 'failed', 'reason': str(exp)}


def get_book(book_id):
    global ses
    try:
        book = ses.query(Book).filter(Book.id == book_id).one()
        book_info = {}
        book_info['book_name'] = book.name
        book_info['authors'] = []
        for author in book.authors:
            book_info['authors'].append(author.id)
        return {'status':'success', 'data': book_info}
    except Exception as exp:
        ses.rollback()
        ses.close()
        print(exp)
        return {'status': 'failed', 'reason': str(exp)}


def save_book(book_id, book_name, authors_ids):
    global ses
    try:
        book = ses.query(Book).filter(Book.id == book_id).one()
        book.name = book_name
        book.authors = []
        if len(authors_ids) > 0:
            authors = ses.query(Author).filter(Author.id.in_(authors_ids)).all()
            print(authors)
            for author in authors:
                book.authors.append(author)
        ses.commit()
        ses.close()
        return {'status': 'success'}
    except Exception as exp:
        ses.rollback()
        ses.close()
        print(exp)
        return {'status': 'failed', 'reason': str(exp)}


def remove_book(book_id):
    global ses
    try:
        book = ses.query(Book).filter(Book.id == book_id).one()
        ses.delete(book)
        ses.commit()
        ses.close()
        return {'status': 'success'}
    except Exception as exp:
        ses.rollback()
        ses.close()
        print(exp)
        return {'status': 'failed', 'reason': str(exp)}


def get_author(author_id):
    global ses
    try:
        author = ses.query(Author).filter(Author.id == author_id).one()
        author_info = {}
        author_info['author_name'] = author.name
        author_info['books'] = []
        for book in author.books:
            author_info['books'].append(book.id)
        return {'status':'success', 'data': author_info}
    except Exception as exp:
        ses.rollback()
        ses.close()
        print(exp)
        return {'status': 'failed', 'reason': str(exp)}


def save_author(author_id, author_name, books_ids):
    global ses
    try:
        author = ses.query(Author).filter(Author.id == author_id).one()
        author.name = author_name
        author.books = []
        print()
        if len(books_ids) > 0:
            books = ses.query(Book).filter(Book.id.in_(books_ids)).all()
            for book in books:
                author.books.append(book)
        for book in author.books:
            print(book.name)
        ses.commit()
        ses.close()
        return {'status': 'success'}
    except Exception as exp:
        ses.rollback()
        ses.close()
        print(exp)
        return {'status': 'failed', 'reason': str(exp)}


def remove_author(author_id):
    global ses
    try:
        author = ses.query(Author).filter(Author.id == author_id).one()
        ses.delete(author)
        ses.commit()
        ses.close()
        return {'status': 'success'}
    except Exception as exp:
        ses.rollback()
        ses.close()
        print(exp)
        return {'status': 'failed', 'reason': str(exp)}
