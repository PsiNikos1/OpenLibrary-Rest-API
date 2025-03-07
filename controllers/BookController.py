from importlib.metadata import files

from Tools.scripts.make_ctype import values
from flask import Blueprint, jsonify, request, session
from flask_restful import http_status_message
from sqlalchemy import text, and_
from sqlalchemy.orm import RelationshipProperty, ColumnProperty

from factories.BookFactory import BookFactory
from model.Book import Book
from model.Author import Author
from model.Work import Work
from initializer.db_init import db


class BookController:
    def __init__(self, app, db):
        self.db = db
        self.book_bp = Blueprint("book_bp", __name__)
        self.app = app

        self.book_bp.add_url_rule("/getAllBooks", "get_books", self.get_books, methods=["GET"])
        self.book_bp.add_url_rule("/getBookByDbId/<int:book_id>", "get_book", self.get_book, methods=["GET"])
        self.book_bp.add_url_rule("/addBook", "add_book", self.add_book, methods=["POST"])
        self.book_bp.add_url_rule("/deleteBookById/<int:book_id>", "delete_book", self.delete_book, methods=["DELETE"])
        self.book_bp.add_url_rule("/getBookByTitle/<string:title>", "get_book_by_title", self.get_book_by_title, methods=["GET"])
        self.book_bp.add_url_rule("/filterBooks", "filter_books", self.filter_books, methods=["GET"])


        app.register_blueprint(self.book_bp)

    def get_books(self):
        books = Book.query.all()
        return jsonify([book.to_dict() for book in books]), 200

    def get_book(self, book_id):
        book = Book.query.get_or_404(book_id)
        return jsonify(book.to_dict()), 200

    def get_book_by_title(self, title):
        book = Book.query.filter(Book.title.ilike(f"%{title}%")).first()
        if book:
            return jsonify(book.to_dict())
        return jsonify({"error": "Book not found"}), 404

    def add_book(self):
        """Adds a new book. Needs at least title, open_library_key, author_name, work_title, author_open_library_key,
         work_open_library_key to be created.
        """
        data = request.get_json()

        title = data.get("title")
        open_library_key = data.get("open_library_key")
        author_name = data.get("author_name")
        work_title = data.get("work_title")

        if not title or not author_name or not work_title or not open_library_key:
            return jsonify({"error": "Title, author_name, and work_title are required but not found"}), 400

        author = Author.query.filter_by(name=author_name).first()
        if not author:
            author = Author(name=author_name, open_library_key=data.get("author_open_library_key"))
            db.session.add(author)
            db.session.commit()

        work = Work.query.filter_by(title=work_title).first()
        if not work:
            work = Work(title=work_title, open_library_key=data.get("work_open_library_key"))
            db.session.add(work)
            db.session.commit()

        book = BookFactory.create_from_json(book_json=data,book_key=data.get("open_library_key"), author=author, work=work)
        return jsonify({"message": f"Book with title '{title}'' added successfully", "book_Db_Id": book.id}), 201

    def filter_books(self):
        """Filters the books for many criteria. It only works as AND filtering and NOT as or"""
        filters = request.get_json()
        r = []
        for field, value in filters.items():
            if hasattr(Book, field):
                attribute = getattr(Book, field)

                if isinstance(Book.__mapper__.attrs[field], RelationshipProperty):
                    r.extend(db.session.query(Book).filter(attribute.has(**value)).all())

                elif isinstance(Book.__mapper__.attrs[field], ColumnProperty):
                    r.extend(db.session.query(Book).filter(attribute == value).all())
        return  jsonify( [book.to_dict() for book in r  ] ), 200

    def delete_book(self, book_id):
        """Deletes a book from its DB id"""
        book = Book.query.get_or_404(book_id)
        db.session.delete(book)
        db.session.commit()
        return jsonify({"message": f"Book with title ' {book.title} 'and id ' {book.id} 'deleted successfully"}), 200
