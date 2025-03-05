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

        self.book_bp.add_url_rule("/getAllBooks", "get_books", self.get_books, methods=["GET"])
        self.book_bp.add_url_rule("/getBookByDbId/<int:book_id>", "get_book", self.get_book, methods=["GET"])
        self.book_bp.add_url_rule("/addBook", "add_book", self.add_book, methods=["POST"])
        self.book_bp.add_url_rule("/deleteBookById/<int:book_id>", "delete_book", self.delete_book, methods=["DELETE"])
        self.book_bp.add_url_rule("/getBookByTitle/<string:title>", "get_book_by_title", self.get_book_by_title, methods=["GET"])

        app.register_blueprint(self.book_bp)

    def get_books(self):
        books = Book.query.all()
        return jsonify([{"title": b.title, "author": b.author.name, "work": b.work.title} for b in books])

    def get_book(self, book_id):
        book = Book.query.get_or_404(book_id)
        return jsonify({"title": book.title, "author": book.author.name, "work": book.work.title})

    def get_book_by_title(self, title):
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
            work = Work(title=work_title, open_library_key=data.get("work_open_library_key"), author_id=author.id)
            db.session.add(work)
            db.session.commit()

        book = Book(
            title=title,
            open_library_key=open_library_key,
            author_id=author.id,
            work_id=work.id,
            publishers=data.get("publishers"),
            number_of_pages=data.get("number_of_pages"),
            isbn_10=data.get("isbn_10"),
            edition_count=data.get("edition_count"),
            subjects=", ".join(data.get("subjects", [])),
            publish_date=data.get("publish_date"),
            cover_id=data.get("cover_id"),
            first_publish_year=data.get("first_publish_year"),
            languages=", ".join(data.get("languages", [])) if data.get("languages") else None,
            lending_edition=data.get("lending_edition"),
            lending_identifier=data.get("lending_identifier"),
            project_gutenberg_ids=", ".join(data.get("project_gutenberg_ids", [])),
            librivox_ids=", ".join(data.get("librivox_ids", [])),
            ia_identifiers=", ".join(data.get("ia_identifiers", [])),
            public_scan=data.get("public_scan", False),
        )

        db.session.add(book)
        db.session.commit()
        return jsonify({"message": f"Book with title '{title}'' added successfully", "book_Db_Id": book.id}), 201



    def delete_book(self, book_id):
        book = Book.query.get_or_404(book_id)
        db.session.delete(book)
        db.session.commit()
        return jsonify({"message": "Book deleted successfully"})
