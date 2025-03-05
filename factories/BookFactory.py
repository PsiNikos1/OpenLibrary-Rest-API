import requests
from initializer.database import db
from model.Author import Author
from model.Work import Work
from model.Book import Book

class BookFactory:

    @staticmethod
    def create_from_json(book_json):

        # Extract book details
        title = book_json.get("title", "Unknown Title")
        book_key = book_json.get("key", "").replace("/works/", "")

        # Extract author details (handling multiple authors)
        author_keys = book_json.get("author_key", [])
        author_names = book_json.get("author_name", [])

        # Ensure at least one author exists
        if not author_keys or not author_names:
            author_keys = [f"unknown_{title.replace(' ', '_')}"]
            author_names = ["Unknown Author"]

        # Ensure author(s) exist
        author_objects = []
        for author_key, author_name in zip(author_keys, author_names):
            # 🔍 Check if author exists (by Open Library Key OR Name)
            author = Author.query.filter(
                (Author.open_library_key == author_key) | (Author.name == author_name)
            ).first()

            if not author:
                author = Author(name=author_name, open_library_key=author_key)
                db.session.add(author)
                db.session.commit()
            author_objects.append(author)

        # Ensure work exists
        work = Work.query.filter_by(open_library_key=book_key).first()
        if not work:
            try:
                work = Work(title=title, open_library_key=book_key, author_id=author_key)
            except Exception as e:
                print(e)
            db.session.add(work)
            db.session.commit()

        # Check if the book already exists
        existing_book = Book.query.filter_by(open_library_key=book_key).first()
        if existing_book:
            return existing_book

        # Create book object
        book = Book(
            title=title,
            author_id=author_objects[0].id,  # Assign first author
            work_id=work.id,
            publishers=", ".join(book_json.get("publishers", [])),
            number_of_pages=book_json.get("number_of_pages"),
            isbn_10=", ".join(book_json.get("isbn_10", [])),
            edition_count=book_json.get("edition_count"),
            subjects=", ".join(book_json.get("subject", [])),
            publish_date=book_json.get("first_publish_year"),
            cover_id=book_json.get("cover_i"),
            open_library_key=book_key,
            first_publish_year=book_json.get("first_publish_year"),
            languages=", ".join(book_json.get("language", [])),
            lending_edition=book_json.get("lending_edition_s"),
            lending_identifier=book_json.get("lending_identifier_s"),
            project_gutenberg_ids=", ".join(book_json.get("id_project_gutenberg", [])),
            librivox_ids=", ".join(book_json.get("id_librivox", [])),
            ia_identifiers=", ".join(book_json.get("ia", [])),
            public_scan=book_json.get("public_scan_b", False),
        )

        # Save book
        db.session.add(book)
        db.session.commit()

        return book
