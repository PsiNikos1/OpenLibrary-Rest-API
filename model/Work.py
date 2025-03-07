from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship
from initializer.database import db
from model.Author import work_author

class Work(db.Model):
    __tablename__ = "work"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    open_library_key = db.Column(db.String(100), unique=True, nullable=False)  # "/works/OL21177W"
    description = db.Column(db.Text)
    first_publish_date = db.Column(db.String(50))
    first_sentence = db.Column(db.Text)

    links = db.Column(db.Text)
    covers = db.Column(db.Text)
    subject_places = db.Column(db.Text)
    subjects = db.Column(db.Text)
    subject_people = db.Column(db.Text)
    subject_times = db.Column(db.Text)
    excerpts = db.Column(db.Text)
    created_at = db.Column(db.DateTime)
    last_modified = db.Column(db.DateTime)

    authors = db.relationship("Author", secondary=work_author, back_populates='works')
    books = db.relationship('Book', back_populates='work')

    def to_dict(self):
        """Convert Work object to a JSON-serializable dictionary."""
        return {
            "id": self.id,
            "title": self.title,
            "open_library_key": self.open_library_key,
            "description": self.description,
            "first_publish_date": self.first_publish_date,
            "first_sentence": self.first_sentence,
            "authors": [author.to_dict() for author in self.authors],  # Include authors
            "links": self.links,
            "covers": self.covers,
            "subject_places": self.subject_places,
            "subjects": self.subjects,
            "subject_people": self.subject_people,
            "subject_times": self.subject_times,
            "excerpts": self.excerpts,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "last_modified": self.last_modified.isoformat() if self.last_modified else None,
        }
