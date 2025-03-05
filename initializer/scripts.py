import requests
from initializer.database import db
from model.Author import Author
from model.Work import Work
from model.Book import Book

# List of subjects to request books from
SUBJECTS = ["fiction", "science", "history", "fantasy", "mystery", "romance", "horror"]


def fetch_books():
    print("Fetching books from Open Library...")
    total_books_fetched = 0

    for subject in SUBJECTS:
        response = requests.get(f"https://openlibrary.org/subjects/{subject}.json?limit=20")
        if response.status_code == 200:
            data = response.json()
            works = data.get("works", [])
            for work in works:
                title = work.get("title", "Unknown Title")
                author_name = work.get("authors", [{}])[0].get("name", "Unknown Author")

                # Ensure author exists
                author = Author.query.filter_by(name=author_name).first()
                if not author:
                    author = Author(name=author_name)
                    db.session.add(author)
                    db.session.commit()

                # Ensure work exists
                work_entry = Work.query.filter_by(title=title).first()
                if not work_entry:
                    work_entry = Work(title=title)
                    db.session.add(work_entry)
                    db.session.commit()

                # Always insert book (even if author/work already exists)
                book = Book(title=title, author_id=author.id, work_id=work_entry.id)
                db.session.add(book)
                total_books_fetched += 1

                if total_books_fetched >= 100:  # Stop when we reach 100 books
                    break

        else:
            print(f"Failed to fetch books for subject '{subject}'. Status Code: {response.status_code}")

        if total_books_fetched >= 100:  # Stop if we have enough books
            break

    db.session.commit()
    print(f" Successfully fetched {total_books_fetched} books!")
