from app import db

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

    def __init__(
        self,
        id,
        isbn,
        title,
        authors,
        publisher,
        num_pages,
        total_copies,
        available_copies,
        cover_image,
    ):
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


if __name__ == "__main__":
    db.create_all()