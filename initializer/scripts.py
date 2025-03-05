import requests

from factories.BookFactory import BookFactory
from initializer.database import db
from model.Author import Author
from model.Work import Work
from model.Book import Book

# List of subjects to request books from
SUBJECTS = ["fiction", "science", "history", "fantasy", "mystery", "romance", "horror"]


def fetch_books(number_of_samples=200):
    print("Fetching books from Open Library...")

    response = requests.get(f"https://openlibrary.org/search.json?q=history?limit={number_of_samples}")
    if response.status_code == 200:
        data = response.json()
        for doc in data["docs"]:
            BookFactory.create_from_json(doc) #Creates new Books & Authors

    db.session.commit()
    total_books = len(response.json()["docs"])
    print(f" Successfully fetched {total_books} books!")
