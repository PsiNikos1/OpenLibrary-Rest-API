from flask import Blueprint, jsonify, request
from model.Book import Book
from model.Author import Author
from model.Work import Work
from initializer.db_init import db


class BookController:
    def __init__(self, app, db):
        self.db = db
        self.book_bp = Blueprint("book_bp", __name__)

        self.book_bp.add_url_rule("/books", "get_books", self.get_books, methods=["GET"])
        self.book_bp.add_url_rule("/books/<int:book_id>", "get_book", self.get_book, methods=["GET"])
        self.book_bp.add_url_rule("/books", "add_book", self.add_book, methods=["POST"])
        self.book_bp.add_url_rule("/books/<int:book_id>", "delete_book", self.delete_book, methods=["DELETE"])

        app.register_blueprint(self.book_bp)

    def get_books(self):
        books = Book.query.all()
        return jsonify([{"title": b.title, "author": b.author.name, "work": b.work.title} for b in books])

    def get_book(self, book_id):
        book = Book.query.get_or_404(book_id)
        return jsonify({"title": book.title, "author": book.author.name, "work": book.work.title})

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
