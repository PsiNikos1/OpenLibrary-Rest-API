from initializer.database import db
from initializer.scripts import fetch_books

def initialize_database(app):
    with app.app_context():
        print("Initializing database...")

        from model.Author import Author
        from model.Work import Work
        from model.Book import Book

        db.create_all()
        fetch_books()
        print(" Tables created successfully!")
