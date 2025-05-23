from initializer.database import db
from model.Author import Author

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

    first_publish_year = db.Column(db.Integer)
    languages = db.Column(db.String(255))
    lending_edition = db.Column(db.String(255))
    lending_identifier = db.Column(db.String(255))
    project_gutenberg_ids = db.Column(db.String(255))
    librivox_ids = db.Column(db.String(255))
    ia_identifiers = db.Column(db.Text)
    public_scan = db.Column(db.Boolean, default=False)
    lccn = db.Column(db.Integer)
    publish_country = db.Column(db.Text)
    by_statement = db.Column(db.Text)
    ocaid = db.Column(db.Text)
    notes = db.Column(db.Text)
    genres = db.Column(db.Text)

    # author = db.relationship("Author", back_populates="works")
    author = db.relationship("Author", back_populates="books")
    work = db.relationship("Work", back_populates="books")

    def to_dict(self):
        author = Author.query.filter_by(id=self.author_id).first()
        return {
            "id": self.id,
            "title": self.title,
            "author": author.name,
            "open_library_key": self.open_library_key
        }