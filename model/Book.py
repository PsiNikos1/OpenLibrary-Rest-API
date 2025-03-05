from initializer.db_init import db

class Book(db.Model):
    __tablename__ = "book"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey("author.id"), nullable=False)  # Correct reference
    work_id = db.Column(db.Integer, db.ForeignKey("work.id"), nullable=False)  # Ensure 'work' is lowercase
