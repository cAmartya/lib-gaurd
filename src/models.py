import bcrypt

from app import db, app
from datetime import datetime


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    username = db.Column(db.String(60), nullable=False)
    password = db.Column(db.String(60), nullable=False)

    def __init__(self, id, name, username, password):
        self.id = id
        self.name = name
        self.username = username
        self.password = password

    def __repr__(self):
        return f"<User {self.username}>"

    def to_json(self):
        return {
            "id": self.id,
            "name": self.name,
            "username": self.username,
        }

    def set_password(self, password):
        self.password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

    def verify_password(self, password):
        return bcrypt.checkpw(password.encode("utf-8"), self.password.encode("utf-8"))


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    isbn = db.Column(db.String(100), nullable=False, unique=True)
    title = db.Column(db.String(100), nullable=False)
    authors = db.Column(db.String(100), nullable=False)
    publisher = db.Column(db.String(100), nullable=False)
    num_pages = db.Column(db.Integer, nullable=False)
    total_copies = db.Column(db.Integer, nullable=False)
    available_copies = db.Column(db.Integer, nullable=False)
    cover_image = db.Column(db.String(100), nullable=False)
    transactions = db.relationship("Transaction", backref="book", cascade="all, delete")

    def __init__(self, id, isbn, title, authors, publisher, num_pages, total_copies, available_copies, cover_image):
        self.id = id
        self.isbn = isbn
        self.title = title
        self.authors = authors
        self.publisher = publisher
        self.num_pages = num_pages
        self.total_copies = total_copies
        self.available_copies = available_copies
        self.cover_image = cover_image

    def __repr__(self):
        return f"<Book {self.id}>"
    
    def to_json(self):
        return {
            "id": self.id, 
            "title": self.title, 
            "isbn": self.isbn, 
            "authors": self.authors, 
            "publisher": self.publisher,
            "num_pages": self.num_pages,
            "total_copies": self.total_copies,
            "available_copies": self.available_copies,
            "cover_image": self.cover_image
        }


class Member(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(60), nullable=False)
    address = db.Column(db.String(200), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    transactions = db.relationship("Transaction", backref="member", cascade="all, delete")

    def __init__(self, id, name, address, phone, email):
        self.id = id
        self.name = name
        self.address = address
        self.phone = phone
        self.email = email

    def __repr__(self):
        return f"<Member {self.id}>"

    def to_json(self):
        return {
            "id": self.id,
            "name": self.name,
            "address": self.address,
            "phone": self.phone,
            "email": self.email,
        }


class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    member_id = db.Column(db.Integer, db.ForeignKey("member.id"), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey("book.id"), nullable=False)
    count = db.Column(db.Integer, nullable=False, default=1)
    issue_date = db.Column(db.Date, nullable=False)
    is_returned = db.Column(db.Boolean, nullable=False, default=False)
    return_date = db.Column(db.Date, nullable=True)
    charges_paid = db.Column(db.Float, nullable=True, default=0)
    issued_by = db.Column(db.String(60), nullable=False)

    def __init__(self, id, member_id, book_id, count, issue_date, return_date, issued_by, charges_paid=0, is_returned=False):
        self.id = id
        self.member_id = member_id
        self.book_id = book_id
        self.count = count
        self.issue_date = issue_date
        self.return_date = return_date
        self.is_returned = is_returned
        self.charges_paid = charges_paid
        self.issued_by = issued_by

    def __repr__(self):
        return f"<Transaction {self.id}>"

    def to_json(self):
        return {
            "id": self.id,
            "member_id": self.member_id,
            "member_name": Member.query.get(self.member_id).name,
            "book_id": self.book_id,
            "count": self.count,
            "issue_date": self.issue_date,
            "return_date": self.return_date,
            "is_returned": self.is_returned,
            "charges_paid": self.charges_paid,
            "issued_by": self.issued_by,
        }

    def calculate_charges(self):
        if self.is_returned:
            return self.charges_paid

        # Calculate no of days from issue date to current date
        days = (datetime.now().date() - self.issue_date).days

        # Total charges = Rent charges + Fine charges
        charges = (min(days, app.config["BOOK_RETURN_DEADLINE"]) * app.config["RENT_PER_DAY"] * self.count)
        + (max(days - app.config["BOOK_RETURN_DEADLINE"], 0) * app.config["FINE_PER_DAY"] * self.count)

        return charges

    def return_book(self) -> bool:
        try:
            if self.is_returned:
                return True
            self.return_date = datetime.now().date()
            self.charges_paid = self.calculate_charges()
            book = Book.query.get(self.book_id)
            book.available_copies += self.count
            self.is_returned = True
            db.session.commit()
            return True
        except Exception as e:
            print(e)
            return False


with app.app_context():
    db.create_all()

if __name__ == "__main__":
    db.create_all()