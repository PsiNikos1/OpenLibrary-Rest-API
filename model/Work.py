from initializer.database import db

class Work(db.Model):
    __tablename__ = "work"

    id = db.Column(db.Integer, primary_key=True)
    open_library_key = db.Column(db.String(255), unique=True, nullable=False)  # /works/OL53919W
    title = db.Column(db.String(255), nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey("author.id"), nullable=False)
    
    author = db.relationship("Author", back_populates="works")
    books = db.relationship("Book", back_populates="work")

