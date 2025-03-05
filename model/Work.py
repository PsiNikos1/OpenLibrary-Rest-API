from initializer.db_init import db


class Work(db.Model):
    __tablename__ = "work"


    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    books = db.relationship('Book', backref='work', lazy=True)