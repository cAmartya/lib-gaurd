from flask import jsonify, make_response, request, flash, render_template
from sqlalchemy.exc import IntegrityError

from models import Book
from app import app, db
from frappe_lib import frappe_client

print("books", app)
# @app.get("/books")
@app.route("/books", methods=["GET"])
def get_books():
    # print("gg")
    # return "books"
    try:
        books = Book.query.limit(8)
        return render_template("books/get.html", books=books)
    except Exception as e:
        print(e)
        return make_response(jsonify({"message": "Internal srver error"}), 500)


# def add_book(isbn, title, authors, publisher, num_pages, total_copies, cover):
#     pass


@app.post("/books/new")
def add_book():
    try:
        title = request.form["title"]
        authors = request.form["authors"]
        isbn = request.form["isbn"]
        publisher = request.form["publisher"]
        num_pages = int(request.form["num_pages"])
        total_copies = int(request.form["total_copies"])
        cover_image = request.files.get("cover_image", None)
        if not title or not authors or not isbn or not publisher or not num_pages or not total_copies:
            # flash("All fields are required", "danger")
            # return render_template("books/new.html")
            return make_response(jsonify({"message": "Fields missing"}), 404)
        
        if cover_image is None:
            cover_image = frappe_client.get_img_from_isbn(isbn)
        
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
    except Exception as e:
        print(e)
    

    pass


@app.get("/books/import")
def import_books():
    try:
        books = frappe_client.get_books()
        # print(books)
        return render_template("books/get.html", books=books)
        
    except Exception as e:
        print(e)
        return make_response(jsonify({"message": "Internal srver error"}), 500)
    pass

@app.route("/books/<int:id>", methods=["GET"])
def show_book(id):
    print(id)
    book = Book.query.get(id)
    return f":{id}"