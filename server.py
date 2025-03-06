from flask import Flask

from controllers.AuthorController import AuthorController
from initializer.db_init import db, initialize_database
from controllers.BookController import BookController
import config  # Ensure config is explicitly imported
from model.Book import Book

app = Flask(__name__)

# Load Configuration
app.config.from_object("config")

# Initialize Database (Only once)
db.init_app(app)
initialize_database(app)

# Register Controllers
book_controller = BookController(app, db)
author_controller = AuthorController(app, db)

if __name__ == "__main__":

    app.run(debug=True)


