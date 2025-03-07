import requests

from factories.BookFactory import BookFactory
from initializer.database import db
from model.Author import Author
from model.Work import Work
from model.Book import Book


# List of subjects to request books from
SUBJECTS = ["fiction", "science", "history", "fantasy", "mystery", "romance", "horror"]


def fetch_books(number_of_samples_per_subject=20):
    print("Fetching books from Open Library...")
    for subject in SUBJECTS:
        response = requests.get(f" https://openlibrary.org/subjects/{subject}.json?limit={number_of_samples_per_subject}")
        if response.status_code == 200:
            for work in response.json()["works"]:
                BookFactory.create_object(work) #Creates new Books & Authors & Work

    db.session.commit()
    total_books = len(response.json()["docs"])
    print(f" Successfully fetched {total_books} books!")
