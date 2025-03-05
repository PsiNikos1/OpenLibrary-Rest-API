import self
from flask import Blueprint, jsonify, request
from model.Book import Book
from model.Author import Author
from model.Work import Work
from initializer.db_init import db


class BookController:
    def __init__(self, app, db):
        self.db = db
        self.book_bp = Blueprint("book_bp", __name__)
        self.app = app

        self.book_bp.add_url_rule("/books", "get_books", self.get_books, methods=["GET"])
        self.book_bp.add_url_rule("/books/<int:book_id>", "get_book", self.get_book, methods=["GET"])
        self.book_bp.add_url_rule("/books", "add_book", self.add_book, methods=["POST"])
        self.book_bp.add_url_rule("/books/<int:book_id>", "delete_book", self.delete_book, methods=["DELETE"])
        self.book_bp.add_url_rule("/books/<string:title>", "get_book_by_title", self.get_book_by_title, methods=["GET"])

        app.register_blueprint(self.book_bp)

    def get_books(self):
        books = Book.query.all()
        return jsonify([{"title": b.title, "author": b.author.name, "work": b.work.title} for b in books])

    def get_book(self, book_id):
        book = Book.query.get_or_404(book_id)
        return jsonify({"title": book.title, "author": book.author.name, "work": book.work.title})

    def get_book_by_title(self, title):
        """ Get a book by title """
        book = Book.query.filter(Book.title.ilike(f"%{title}%")).first()
        if book:
            return jsonify({
                "id": book.id,
                "title": book.title,
                "author_id": book.author_id,
                "work_id": book.work_id,
                "publishers": book.publishers,
                "number_of_pages": book.number_of_pages,
                "isbn_10": book.isbn_10,
                "edition_count": book.edition_count,
                "subjects": book.subjects,
                "publish_date": book.publish_date,
                "cover_id": book.cover_id,
                "open_library_key": book.open_library_key,
                "first_publish_year": book.first_publish_year,
                "languages": book.languages,
                "lending_edition": book.lending_edition,
                "lending_identifier": book.lending_identifier,
                "project_gutenberg_ids": book.project_gutenberg_ids,
                "librivox_ids": book.librivox_ids,
                "ia_identifiers": book.ia_identifiers,
                "public_scan": book.public_scan,
            })
        return jsonify({"error": "Book not found"}), 404

    def add_book(self):
        data = request.get_json()
        author = Author.query.filter_by(name=data["author"]).first()
        if not author:
            author = Author(name=data["author"])
            db.session.add(author)
            db.session.commit()

        work = Work.query.filter_by(title=data["work"]).first()
        if not work:
            work = Work(title=data["work"])
            db.session.add(work)
            db.session.commit()

        book = Book(title=data["title"], author_id=author.id, work_id=work.id)
        db.session.add(book)
        db.session.commit()
        return jsonify({"message": "Book added successfully"}), 201

    def delete_book(self, book_id):
        book = Book.query.get_or_404(book_id)
        db.session.delete(book)
        db.session.commit()
        return jsonify({"message": "Book deleted successfully"})
