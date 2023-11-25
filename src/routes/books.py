import os
from urllib.parse import urlencode
from flask import jsonify, make_response, request, flash, render_template, redirect
from sqlalchemy.exc import IntegrityError

from models import Book, Member
from app import app, db
from frappe_lib import frappe_client

@app.get("/books")
# @app.route("/books", methods=["GET", "DELETE"])
def get_books():
    query_key = request.args.get("key")
    q = request.args.get("query")
    page = request.args.get("page", None)
    if page is None:
        page = 1
    page = int(page)
    print("books page", page, type(page))
    try:
        if query_key == "title":
            books = Book.query.filter(Book.title.like("%{}%".format(q))).offset((page-1)*8).limit(8)
        elif query_key == "authors":
            books = Book.query.filter(Book.authors.like("%{}%".format(q))).offset((page-1)*8).limit(8)
        elif query_key == "isbn":
            books = Book.query.filter(Book.isbn.like("%{}%".format(q))).offset((page-1)*8).limit(8)
        elif query_key == "publisher":
            books = Book.query.filter(Book.publisher.like("%{}%".format(q))).offset((page-1)*8).limit(8)
        else:
            books = Book.query.offset((page-1)*8).limit(8)
        books = [Book.to_json(book) for book in books]
        query_str=""
        if query_key and q:
            query_str = urlencode({'key':query_key, 'query':q})
        members = [Member.to_json(ele) for ele in Member.query.all()]
        return render_template("books/get.html", books=books, page=page, query_str=query_str, members=members)
    except Exception as e:
        print(e)
        return make_response(jsonify({"message": "Internal srver error"}), 500)


@app.route("/books/new", methods=["GET", "POST"])
def add_book():
    if request.method == "GET":
        return render_template("books/new.html")
    try:
        title = request.form["title"]
        authors = request.form["authors"]
        isbn = request.form["isbn"]
        publisher = request.form["publisher"]
        num_pages = request.form["num_pages"]
        total_copies = request.form["total_copies"]
        cover_image = request.files.get("cover_image", None)
        # cover_image = request.files["cover_image"]
        print(title, authors, isbn, publisher, num_pages, total_copies)
        if not title or not authors or not isbn or not publisher or not num_pages or not total_copies:
            # flash("All fields are required", "danger")
            # return render_template("books/new.html")
            return make_response(jsonify({"message": "Fields missing"}), 404)
        if num_pages == '':
            num_pages = 0
        if total_copies == '':
            total_copies = 1
        print(cover_image, type(cover_image))
        if cover_image is None:
            frappe_client.get_img_from_isbn(app.config['UPLOAD_FOLDER'], isbn)
        else:
            cover_image.save(os.path.join(app.config['UPLOAD_FOLDER'], isbn))
        
        filename = isbn
        book = Book(
            id=None,
            title=title,
            authors=authors,
            isbn=isbn,
            publisher=publisher,
            num_pages=num_pages,
            total_copies=total_copies,
            available_copies=total_copies,
            cover_image=filename
        )
        db.session.add(book)
        db.session.commit()
    except IntegrityError:
        print(book, "already exists")
        # flash("Book already exists", "warning")
        # return make_response(jsonify({"message": "already exists"}), 404)
    except Exception as e:
        print(e)
        return make_response(jsonify({"message": e}), 500)
    finally:
        return redirect("/books")

# @app.get("/books/import")
@app.route("/books/import", methods=["GET"])
def import_books():
    query = dict()
    query_key = request.args.get("key")
    q = request.args.get("query")
    if query_key and q:
        query.setdefault(query_key, q)
    page = request.args.get("page", None)
    if page is None:
        page = 1
    page = int(page)
    query.setdefault("page", page)
    print("import page", page, type(page), query)
    try:
        books = frappe_client.get_books(query=query)
        query_str=""
        if query_key and q:
            query_str = urlencode({'key':query_key, 'query':q})
        return render_template("books/get.html", books=books, page=page, query_str=query_str, members=[])
        
    except Exception as e:
        print(e)
        return make_response(jsonify({"message": "Internal srver error"}), 500)
    pass

@app.route("/books/<int:id>", methods=["GET", "POST", "DELETE"])
def show_book(id):
    print(id)
    if request.method == "POST":
        book = Book.query.get(id)
        book.title = request.form["title"]
        book.authors = request.form["authors"]
        book.isbn = request.form["isbn"]
        book.publisher = request.form["publisher"]
        book.num_pages = request.form["num_pages"]
        book.total_copies = request.form["total_copies"]
        new_cover_image = request.files.get("cover_image", None)
        if new_cover_image:
            new_cover_image.save(os.path.join(app.config['UPLOAD_FOLDER'], book.cover_image))
        db.session.commit()
        return redirect("/books")
        # return make_response(jsonify({"message": book}))
        return render_template("books/get.html")
    elif request.method == "DELETE":
        book = Book.query.get(id)
        db.session.delete(book)
        db.session.commit()
        print(id, book)
        
        # return redirect("/books")
        return make_response(jsonify({"message": "success"}))
    elif request.method == "GET":
        book = Book.query.get(id)
        return render_template("books/new.html", book=book)
