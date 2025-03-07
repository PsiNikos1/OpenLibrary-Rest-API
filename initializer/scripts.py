import requests

from factories.BookFactory import BookFactory
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

    print(f" Successfully fetched {Book.query.count()} books!")
