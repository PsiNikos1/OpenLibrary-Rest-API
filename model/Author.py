from flask import jsonify

from initializer.database import db

work_author = db.Table(
    "work_author",
    db.Column("work_id", db.Integer, db.ForeignKey("work.id"), primary_key=True),
    db.Column("author_id", db.Integer, db.ForeignKey("author.id"), primary_key=True)
)


class Author(db.Model):
    __tablename__ = "author"

    id = db.Column(db.Integer, primary_key=True)
    personal_name = db.Column(db.String(255))
    name = db.Column(db.String(255), nullable=False, unique=True)
    open_library_key = db.Column(db.String(255), unique=True, nullable=False)  # authors/OL18319A
    birth_date = db.Column(db.String(50))
    bio = db.Column(db.Text)
    fuller_name = db.Column(db.String(255))

    works = db.relationship("Work", secondary=work_author, back_populates='authors')
    books = db.relationship("Book", back_populates="author", lazy="dynamic")

    def to_dict(self):
        return {
            "id": self.id,
            "open_library_key": self.open_library_key,
            "name": self.name,
            "personal_name": self.personal_name,
            "birth_date": self.birth_date,
            "bio": self.bio,
            "fuller_name": self.fuller_name,
            "works": [work.to_dict() for work in self.works],
            "books": [book.to_dict() for book in self.books]
        }
