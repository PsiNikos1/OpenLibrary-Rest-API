import json

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
            break


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

        existing_book = Book.query.filter_by(open_library_key=book_key, title= book_json.get("title")).first()
        if existing_book:
            return existing_book

        title = book_json.get("title")
        if title is None or title == "":
            raise Exception(f"Book title must not be null. Book key is '{book_key}'")

        author_id = author.id
        work_id = work.id
        open_library_key = book_key

        publishers = ",".join(book_json.get("publishers")) if isinstance(book_json.get("publishers"), list) else book_json.get("publishers")
        number_of_pages = ",".join(book_json.get("number_of_pages")) if isinstance(book_json.get("number_of_pages"), list) else book_json.get("number_of_pages")
        isbn_10 = ",".join(book_json.get("isbn_10")) if isinstance(book_json.get("isbn_10"), list) else book_json.get("isbn_10")
        genres = ",".join(book_json.get("genres")) if isinstance(book_json.get("genres"), list) else book_json.get("genres")
        lccn = ",".join(book_json.get("lccn")) if isinstance(book_json.get("lccn"), list) else book_json.get("lccn")
        notes = ",".join(book_json.get("notes")) if isinstance(book_json.get("notes"), list) else book_json.get("notes")
        languages = ",".join(book_json.get("languages")) if isinstance(book_json.get("languages"), list) else book_json.get("languages")
        # subjects = book_json.get("subjects")
        publish_date = ",".join(book_json.get("publish_date")) if isinstance(book_json.get("publish_date"), list) else book_json.get("publish_date")
        publish_country = ",".join(book_json.get("publish_country")) if isinstance(book_json.get("publish_country"), list) else book_json.get("publish_country")
        by_statement = ",".join(book_json.get("by_statement")) if isinstance(book_json.get("by_statement"), list) else book_json.get("by_statement")
        ocaid = ",".join(book_json.get("ocaid")) if isinstance(book_json.get("ocaid"), list) else book_json.get("ocaid")



        book = Book(
            title=title,
            open_library_key= open_library_key,
            author_id=author_id,
            work_id=work_id,
            publishers=publishers,
            number_of_pages=number_of_pages,
            isbn_10=isbn_10,
            edition_count=",".join(book_json.get("edition_count")) if isinstance(book_json.get("edition_count"), list) else book_json.get("edition_count"),
            # subjects=subjects,
            publish_date=publish_date,
            first_publish_year=book_json.get("first_publish_year"),
            languages=languages,
            lending_edition=",".join(book_json.get("lending_edition")) if isinstance(book_json.get("lending_edition"), list) else book_json.get("lending_edition"),
            lending_identifier=",".join(book_json.get("lending_identifier")) if isinstance(book_json.get("lending_identifier"), list) else book_json.get("lending_identifier"),
            project_gutenberg_ids=",".join(book_json.get("project_gutenberg_ids")) if isinstance(book_json.get("project_gutenberg_ids"), list) else book_json.get("project_gutenberg_ids"),
            librivox_ids=",".join(book_json.get("librivox_ids")) if isinstance(book_json.get("librivox_ids"), list) else book_json.get("librivox_ids"),
            ia_identifiers=",".join(book_json.get("ia_identifiers")) if isinstance(book_json.get("ia_identifiers"), list) else book_json.get("ia_identifiers"),
            public_scan=",".join(book_json.get("public_scan")) if isinstance(book_json.get("public_scan"), list) else book_json.get("public_scan"),
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
