from importlib.metadata import files

from Tools.scripts.make_ctype import values
from flask import Blueprint, jsonify, request, session
from flask_restful import http_status_message
from sqlalchemy import text, and_
from sqlalchemy.orm import RelationshipProperty

from model.Book import Book
from model.Author import Author
from model.Work import Work
from initializer.db_init import db


class AuthorController:
    def __init__(self, app, db):
        self.db = db
        self.author_bp = Blueprint("author_bp", __name__)
        self.app = app

        self.author_bp.add_url_rule("/getAllAuthors", "get_authors", self.get_authors, methods=["GET"])
        self.author_bp.add_url_rule("/getBookByDbId/<int:book_id>", "get_book", self.get_book, methods=["GET"])
        self.author_bp.add_url_rule("/addBook", "add_book", self.add_book, methods=["POST"])
        self.author_bp.add_url_rule("/deleteBookById/<int:book_id>", "delete_book", self.delete_book, methods=["DELETE"])
        self.author_bp.add_url_rule("/getBookByTitle/<string:title>", "get_book_by_title", self.get_book_by_title, methods=["GET"])
        self.author_bp.add_url_rule("/filter", "filter_books", self.filter_books, methods=["GET"])


        app.register_blueprint(self.author_bp)

    def get_authors(self):
        authors = Author.query.all()
        return jsonify([author.to_dict() for author in authors])

    def get_author(self, author_id):
        author = Author.query.get_or_404(author_id)
        return jsonify(author.to_dict())

   