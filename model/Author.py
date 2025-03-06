from initializer.database import db

class Author(db.Model):
    __tablename__ = "author"

    id = db.Column(db.Integer, primary_key=True)
    open_library_key = db.Column(db.String(255), unique=True, nullable=False)  # authors/OL18319A
    name = db.Column(db.String(255), nullable=False, unique=True)
    books = db.relationship("Book", back_populates="author")
    works = db.relationship("Work", back_populates="author")

    def to_dict(self):
        return {
            "id": self.id,
            "open_library_key": self.open_library_key,
            "name": self.name
        }

