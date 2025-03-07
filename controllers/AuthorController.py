from flask import Blueprint, jsonify, request, session
from model.Author import Author
from initializer.db_init import db


class AuthorController:
    def __init__(self, app, db):
        self.db = db
        self.author_bp = Blueprint("author_bp", __name__)
        self.app = app

        self.author_bp.add_url_rule("/getAllAuthors", "get_authors", self.get_authors, methods=["GET"])
        self.author_bp.add_url_rule("/getAuthorByDbId/<int:author_id>", "get_author", self.get_author, methods=["GET"])
        self.author_bp.add_url_rule("/filterAuthors", "filter_authors", self.filter_authors, methods=["GET"])

        # self.author_bp.add_url_rule("/addAuthor", "get_author", self.add_book, methods=["POST"])
        # self.author_bp.add_url_rule("/deleteBookById/<int:book_id>", "delete_book", self.delete_book, methods=["DELETE"])
        # self.author_bp.add_url_rule("/getBookByTitle/<string:title>", "get_book_by_title", self.get_book_by_title, methods=["GET"])


        app.register_blueprint(self.author_bp)

    def get_authors(self):
        authors = Author.query.all()
        return jsonify([author.to_dict() for author in authors])

    def get_author(self, author_id):
        author = Author.query.get_or_404(author_id)
        return jsonify(author.to_dict())

    def filter_authors(self):
        """Filters the authors with many criteria. It only works as AND filtering and NOT as or"""
        filters = request.get_json()
        r = []
        for field, value in filters.items():
            if hasattr(Author, field):
                attribute = getattr(Author, field)
                r.extend( db.session.query(Author).filter(attribute == value).all() )
        print(r)
        return  jsonify( [author.to_dict() for author in r] ), 200
