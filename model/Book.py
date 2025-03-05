import requests

from initializer.db import db
from model.Author import Author


def get_author(author_id: str) -> Author:
    authors_url = f'https://openlibrary.org/authors/'
    res = requests.get(f"{authors_url}/{author_id}.json")
    return Author.from_dict(res.json())


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(300), nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('author.id'), nullable=True)
    author = db.relationship('Author', backref=db.backref('books', lazy=True))
    openlibrary_id = db.Column(db.String(50), unique=True, nullable=False)
    publish_date = db.Column(db.String(50))
    number_of_pages = db.Column(db.Integer)
    subjects = db.Column(db.String(500))  # Storing subjects as a comma-separated string
    work_id = db.Column(db.String(50))
    isbn_10 = db.Column(db.String(20))
    publishers = db.Column(db.String(200))  # Storing publishers as a comma-separated string
    publish_places = db.Column(db.String(200))  # Storing publish places as a comma-separated string
    genres = db.Column(db.String(200))  # Storing genres as a comma-separated string
    languages = db.Column(db.String(50))  # Storing languages as a comma-separated string

    @classmethod
    def from_dict(cls, data):
        if not data:
            raise ValueError("Invalid data: Received None instead of a dictionary")

        # Extract author ID properly
        author_key = data.get("authors", [{}])[0].get("key", None)
        author_id = author_key.split("/")[-1] if author_key else None
        cls.author = get_author(author_id=author_id)
        # Extract work ID properly
        work_key = data.get("works", [{}])[0].get("key", None)
        work_id = work_key.split("/")[-1] if work_key else None

        return cls(
            title=data.get("title"),
            author_id=author_id,
            openlibrary_id=data.get("key", "").split("/")[-1],
            publish_date=data.get("publish_date"),
            number_of_pages=data.get("number_of_pages"),
            subjects=", ".join(data.get("subjects", [])),
            work_id=work_id,
            isbn_10=", ".join(data.get("isbn_10", [])),
            publishers=", ".join(data.get("publishers", [])),
            publish_places=", ".join(data.get("publish_places", [])),
            genres=", ".join(data.get("genres", [])),
            languages=", ".join(
                [lang.get("key", "").split("/")[-1] for lang in data.get("languages", []) if "key" in lang])
        )
