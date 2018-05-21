from flask import render_template, Response, abort, redirect, session, abort, request, url_for
import requests
from copy import copy
from flask import jsonify
import json
from app import app
import os
from datetime import datetime
from app.entities import *
from app.backend import db_manager
import flask_login
from flask_login import LoginManager
from flask_login import UserMixin, login_manager, login_required, login_user, logout_user


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


@login_manager.user_loader
def load_user(user_id):
    print("User loaded")
    return User.get(user_id)


@app.route("/login", methods=["GET", "POST"])
def login():
      print("Aaaa")
      error_message = ""
      if request.method == "POST":
        login = request.form["login"]
        password = request.form["password"]
        if "remember" in request.form.keys():
            remember_me = request.form["remember"]
        else:
            remember_me = False

        user = User.get_user_from_login_data(login, password)
        print(user)

        if user:
          login_user(user, remember=remember_me)
          next = request.args.get('next')
          return redirect(next or url_for("RenderMainTemplate"))
        else:
            error_message = "Не верный логин или пароль"
      return render_template("login.html", error_message=error_message)

@app.route("/")
@app.route("/index")
@login_required
def RenderMainTemplate():
    print("Hello")
    return render_template("index.html", title="Libruary");


@app.route("/books")
@login_required
def render_books():
    return render_template("books.html")


@app.route("/authors")
@login_required
def render_authors():
    return render_template("authors.html")


@app.route("/add_book", methods=['GET', 'POST'])
def add_book():
    if request.method == "POST":
        book_name = request.form["book_name"]
        if book_name is None or len(book_name) == 0:
            return json.dumps({"status": "failed", "reason": "Book name is empty"})

        authors_ids = []
        if "authors_ids" in request.form.keys():
            authors_ids = request.form["authors_ids"]
            authors_ids = json.loads(authors_ids)
            authors_ids = [int(_) for _ in authors_ids]

        add_result = db_manager.add_book(book_name, authors_ids)

        return json.dumps(add_result)


@app.route("/add_author", methods=['GET', 'POST'])
def add_author():
    if request.method == "POST":
        author_name = request.form["author_name"]
        if author_name is None or len(author_name) == 0:
            return json.dumps({"status": "failed", "reason": "Author name is empty"})

        books_ids = []
        if "books_ids" in request.form.keys():
            books_ids = request.form["books_ids"]
            books_ids = json.loads(books_ids)
            books_ids = [int(_) for _ in books_ids]

        add_result = db_manager.add_author(author_name, books_ids)

        return json.dumps(add_result)


@app.route("/load_books", methods=['GET', 'POST'])
def load_books():
    if request.method == "POST":
        return json.dumps(db_manager.load_books())
    else:
        return json.dumps("Not allowed method")


@app.route("/load_authors", methods=['GET', 'POST'])
def load_authors():
    if request.method == "POST":
        return json.dumps(db_manager.load_authors())
    else:
        return json.dumps("Not allowed method")


@app.route("/load_table_data", methods=['GET', 'POST'])
def load_table_data():
    if request.method == "POST":
        return json.dumps(db_manager.load_data_for_table())
    else:
        return json.dumps("Not allowed method")


@app.route("/get_book", methods=['GET', 'POST'])
def get_book():
    if request.method == "POST":
        book_id = request.form["book_id"]
        return json.dumps(db_manager.get_book(book_id))
    else:
        return json.dumps("Not allowed method")


@app.route("/save_book", methods=['GET', 'POST'])
def save_book():
    if request.method == "POST":
        book_name = request.form["book_name"]
        book_id = request.form["book_id"]
        if book_name is None or len(book_name) == 0:
            return json.dumps({"status": "failed", "reason": "Book name is empty"})

        authors_ids = []
        if "authors_ids" in request.form.keys():
            authors_ids = request.form["authors_ids"]
            authors_ids = json.loads(authors_ids)
            authors_ids = [int(_) for _ in authors_ids]
        return  json.dumps(db_manager.save_book(book_id, book_name, authors_ids))
    else:
        return json.dump("Not allowed method")


@app.route("/remove_book", methods=['GET', 'POST'])
def remove_book():
    if request.method == "POST":
        book_id = request.form["book_id"]
        return  json.dumps(db_manager.remove_book(book_id))
    else:
        return json.dump("Not allowed method")


@app.route("/get_author", methods=['GET', 'POST'])
def get_author():
    if request.method == "POST":
        author_id = request.form["author_id"]
        return json.dumps(db_manager.get_author(author_id))
    else:
        return json.dumps("Not allowed method")


@app.route("/save_author", methods=['GET', 'POST'])
def save_author():
    if request.method == "POST":
        author_name = request.form["author_name"]
        author_id = request.form["author_id"]
        if author_name is None or len(author_name) == 0:
            return json.dumps({"status": "failed", "reason": "Author name is empty"})

        books_ids = []
        if "books_ids" in request.form.keys():
            books_ids = request.form["books_ids"]
            books_ids = json.loads(books_ids)
            books_ids = [int(_) for _ in books_ids]
        return json.dumps(db_manager.save_author(author_id, author_name, books_ids))
    else:
        return json.dump("Not allowed method")


@app.route("/remove_author", methods=['GET', 'POST'])
def remove_author():
    if request.method == "POST":
        author_id = request.form["author_id"]
        return json.dumps(db_manager.remove_author(author_id))
    else:
        return json.dump("Not allowed method")



@app.route("/find")
def find():
    if request.method == "POST":
        user_request = request.form["user_request"]
        by_whom = request.form["by_whom"]
        return json.dumps(db_manager.find_books(user_request, by_whom))
    else:
        return json.dump("Not allowed method")
