from flask import jsonify, make_response, request, flash, render_template, redirect
from sqlalchemy.exc import IntegrityError

from models import Book
from app import app, db
from frappe_lib import frappe_client

@app.get("/books")
# @app.route("/books", methods=["GET", "DELETE"])
def get_books():
    try:
        books = Book.query.limit(8)
        books = [{
                    "id": book.id, 
                    "title": book.title, 
                    "isbn": book.isbn, 
                    "authors": book.authors, 
                    "publisher": book.publisher,
                    "num_pages": book.num_pages,
                    "total_copies": book.total_copies,
                    "available_copies": book.available_copies,
                    "cover_image": book.cover_image
                } for book in books]
        return render_template("books/get.html", books=books)
    except Exception as e:
        print(e)
        return make_response(jsonify({"message": "Internal srver error"}), 500)


@app.post("/books/new")
def add_book():
    try:
        title = request.form["title"]
        authors = request.form["authors"]
        isbn = request.form["isbn"]
        publisher = request.form["publisher"]
        num_pages = request.form["num_pages"]
        total_copies = request.form["total_copies"]
        cover_image = request.files.get("cover_image", None)
        print(title, authors, isbn, publisher, num_pages, total_copies)
        if not title or not authors or not isbn or not publisher or not num_pages or not total_copies:
            # flash("All fields are required", "danger")
            # return render_template("books/new.html")
            return make_response(jsonify({"message": "Fields missing"}), 404)
        if num_pages == '':
            num_pages = 0
        if total_copies == '':
            total_copies = 1
        if cover_image is None:
            frappe_client.get_img_from_isbn(app.config['UPLOAD_FOLDER'], isbn)
        
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

@app.get("/books/import")
def import_books():
    query = dict()
    query_key = request.args.get("key")
    q = request.args.get("query")
    if query_key and q:
        query.setdefault(query_key, q)
    try:
        books = frappe_client.get_books(query=query)
        return render_template("books/get.html", books=books)
        
    except Exception as e:
        print(e)
        return make_response(jsonify({"message": "Internal srver error"}), 500)
    pass

@app.route("/books/<int:id>", methods=["GET", "PUT", "DELETE"])
def show_book(id):
    print(id)
    if request.method == "PUT":
        book = Book.query.get(id)
        book.title = request.form["title"]
        book.authors = request.form["authors"]
        book.isbn = request.form["isbn"]
        book.publisher = request.form["publisher"]
        book.num_pages = request.form["num_pages"]
        book.total_copies = request.form["total_copies"]
        book.cover_image = request.files.get("cover_image", None)
        db.session.commit()
        return make_response(jsonify({"message": book}))
        return render_template("books/get.html")
    elif request.method == "DELETE":
        book = Book.query.get(id)
        db.session.delete(book)
        db.session.commit()
        print(id, book)
        
        # return redirect("/books")
        return make_response(jsonify({"message": "success"}))