import requests

from factories.WorkFactory import WorkFactory
from factories.AuthorFactory import AuthorFactory
from initializer.database import db
from model.Author import Author
from model.Work import Work
from model.Book import Book

class BookFactory:

    @staticmethod
    def create_object(work_json):

        title = work_json.get("title")
        book_key = work_json.get("key", "").replace("/works/", "")
        authors = work_json["authors"]
        db_authors = []
        for work_author in authors:
            new_author = Author.query.filter(
                (Author.open_library_key == work_author.get("key").replace("/authors/", "")) | (Author.name == work_author.get("name"))
            ).first()
            if new_author:
                db_authors.append(new_author)
                continue
            author_url = work_author.get("key")
            response = requests.get(f" https://openlibrary.org/{author_url}.json")
            new_author = AuthorFactory.create_from_json(response.json())
            db.session.add(new_author)
            db.session.commit()
            db_authors.append(new_author)

        work = Work.query.filter_by(open_library_key=book_key).first()
        if not work:
            work = WorkFactory.create_from_json(work_json, authors=db_authors)
            db.session.add(work)
            db.session.commit()

        response = requests.get(f" https://openlibrary.org/books/{book_key}.json")
        new_book = BookFactory.create_from_json(response.json(), book_key, db_authors[-1], work)
        return new_book

    @staticmethod
    def create_from_json(book_json: dict, book_key, author: Author, work:Work)-> Book:

        existing_book = Book.query.filter_by(open_library_key=book_key).first()
        if existing_book:
            return existing_book

        title = book_json.get("title")
        if title is None or title == "":
            raise Exception(f"Book title must not be null. Book key is '{book_key}'")

        author_id = author.id
        work_id = work.id
        open_library_key = book_key

        publishers = book_json.get("publishers")
        number_of_pages = book_json.get("number_of_pages")
        isbn_10 = book_json.get("isbn_10")
        subject_place = book_json.get("subject_place")
        covers = book_json.get("covers")
        genres = book_json.get("genres")
        lccn = book_json.get("lccn")
        notes = book_json.get("notes")
        languages = book_json.get("languages")
        subjects = book_json.get("subjects")
        publish_date = book_json.get("publish_date")
        publish_country = book_json.get("publish_country")
        by_statement = book_json.get("by_statement")
        ocaid = book_json.get("ocaid")



        book = Book(
            title=title,
            open_library_key= open_library_key,
            author_id=author_id,
            work_id=work_id,
            publishers=publishers,
            number_of_pages=number_of_pages,
            isbn_10=isbn_10,
            edition_count=book_json.get("edition_count"),
            subjects=subjects,
            publish_date=publish_date,
            cover_id=covers,
            first_publish_year=book_json.get("first_publish_year"),
            languages=languages,
            lending_edition=book_json.get("lending_edition_s"),
            lending_identifier=book_json.get("lending_identifier_s"),
            project_gutenberg_ids=book_json.get("id_project_gutenberg"),
            librivox_ids=book_json.get("id_librivox", []),
            ia_identifiers=book_json.get("ia", []),
            public_scan=book_json.get("public_scan_b"),
            lccn=lccn,
            publish_country = publish_country,
            by_statement=by_statement,
            ocaid=ocaid,
            notes=notes,
            genres=genres
        )
        db.session.add(book)
        db.session.commit()
        return book
