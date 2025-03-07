--ABOUT

This project is a Flask-based API that allows users to CRUD Books and Authors. The contents of the database are fetched
from OpenLibrary. More specific the database is filled with 110  books in total with its authors and work. This procedure
takes almost 3 minutes to complete. The API is able to CRUD Users & Books with https requests.
If you like to  change the total amount of  book that are fetched to reduce the amount of time it takes to fetch data,
you can change the total books per subject in the script.py

--ORM MODEL
Author - Work (Many-To-Many)
Work - Book (One-to-Many)
Author - Book (One-to-Many)
I used Flask & SQLAlchemy framework as the database

--INSTALL REQUIREMENTS
This API was developed in python 3.10.10.
Run the command ' pip install -r requirements.txt '.
Run the command ' python ./server.py ' to start the server.

--ENDPOINTS
The API has 9 endpoints, 6 for managing Books and 3 for managing Authors. More specific (Assuming http://127.0.0.1:5000/
is our main url):
1-> http://127.0.0.1:5000/getAllAuthors, returns all Authors that are store in our local database.
2-> http://127.0.0.1:5000/getAuthorByDbId/<int:author_id>, returns the specified Author based on it db id.
3-> http://127.0.0.1:5000/filterAuthors,
4-> http://127.0.0.1:5000/getAllBooks,  returns all Books that are store in our local database.
5-> http://127.0.0.1:5000/getBookByDbId/<int:book_id>, returns the specified Book based on it db id.
6-> http://127.0.0.1:5000/getBookByTitle/<string:title>, returns the specified Book based on its title.
7-> http://127.0.0.1:5000/getBookByTitle/deleteBookById/<int:book_id>, deletes a specified Book by its db id.
8-> http://127.0.0.1:5000/addBook, requires a json body and adds a Book to the local database.
9-> http://127.0.0.1:5000/filterBooks, requires a json body to do an AND query and return the Book that fullfill that query.

--JSON EXAMPLES
3->
    {
        "name": "Jane Austen",
        "open_library_key": "OL19767A",
        "personal_name": "Doyle, Arthur Conan"
    }
6-> http://127.0.0.1:5000/getBookByTitle/Emma
8->
    {
        "title": "Hello World",
        "open_library_key": "randomkey",
        "author_name": "WINGS",
        "work_title": "Restful API",
        "work_open_library_key": "randomWorkKey",
        "author_open_library_key":"randomAuthorKey"
    }
9->
    {
            "author": {
                "name":"WINGS"
                },
            "open_library_key": "randomkey",
            "title": "Hello World"
    }

