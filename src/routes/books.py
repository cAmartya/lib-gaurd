from flask import jsonify, make_response, request, flash
from sqlalchemy.exc import IntegrityError

from models import Book
from app import app, db
from frappe_lib import frappe_client

@app.get("/books")
def get_books():
    try:
        books = Book.query.all()
        return jsonify([book.json() for book in books])
    except Exception as e:
        print(e)
        return make_response(jsonify({"message": "Internal srver error"}), 500)


@app.post("/books/new")
def add_book():
    try:
        title = request.form["title"]
        authors = request.form["authors"]
        isbn_code = request.form["isbn_code"]
        publisher = request.form["publisher"]
        num_pages = int(request.form["num_pages"])
        total_copies = int(request.form["total_copies"])
        cover_image = request.files.get("cover_image", None)
        if not title or not authors or not isbn_code or not publisher or not num_pages or not total_copies:
            # flash("All fields are required", "danger")
            # return render_template("books/new.html")
            return make_response(jsonify({"message": "Fields missing"}), 404)
        
        if cover_image is None:
            cover_image = frappe_client.get_img_from_isbn(isbn_code)
        
        filename = isbn_code
        book = Book(
            id=None,
            title=title,
            authors=authors,
            isbn=isbn_code,
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
    except Exception as e:
        print(e)
    

    pass


@app.get("/books/import")
def import_books():
    try:
        books = frappe_client.get_books()
        
    except:
        return make_response(jsonify({"message": "Internal srver error"}), 500)
    pass

