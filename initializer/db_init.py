from initializer.database import db
from initializer.scripts import fetch_books

def initialize_database(app):
    with app.app_context():
        print("Initializing database...")
        db.drop_all()
        db.create_all()
        fetch_books()
        print(" Tables created successfully!")
