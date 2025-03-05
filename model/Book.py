from initializer.database import db
from model.Author import Author
from model.Work import Work


class Book(db.Model):
    __tablename__ = "book"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey("author.id"), nullable=False)
    work_id = db.Column(db.Integer, db.ForeignKey("work.id"), nullable=False)
    open_library_key = db.Column(db.String(255), unique=True, nullable=False)

    publishers = db.Column(db.String(255))
    number_of_pages = db.Column(db.Integer)
    isbn_10 = db.Column(db.String(50))
    edition_count = db.Column(db.Integer)
    subjects = db.Column(db.Text)
    publish_date = db.Column(db.String(50))
    cover_id = db.Column(db.String(255))
    open_library_key = db.Column(db.String(255), unique=True, nullable=False)

    first_publish_year = db.Column(db.Integer)
    languages = db.Column(db.String(255))
    lending_edition = db.Column(db.String(255))
    lending_identifier = db.Column(db.String(255))
    project_gutenberg_ids = db.Column(db.String(255))
    librivox_ids = db.Column(db.String(255))
    ia_identifiers = db.Column(db.Text)
    public_scan = db.Column(db.Boolean, default=False)

    author = db.relationship("Author", back_populates="books")
    work = db.relationship("Work", back_populates="books")
