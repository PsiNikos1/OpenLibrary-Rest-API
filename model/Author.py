from initializer.db import db


# ORM Models
class Author(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    birth_date = db.Column(db.String(50))
    death_date = db.Column(db.String(50))
    bio = db.Column(db.Text)
    remote_ids = db.Column(db.String(500))  # Store as a JSON string
    alternate_names = db.Column(db.String(500))  # Store as a comma-separated string
    openlibrary_id = db.Column(db.String(50), unique=True, nullable=False)
    photograph = db.Column(db.String(300))  # Store URL to the photograph

    @classmethod
    def from_dict(cls, data):
        if not data:
            raise ValueError("Invalid data: Received None instead of a dictionary")

        return cls(
            name=data.get("name"),
            birth_date=data.get("birth_date"),
            death_date=data.get("death_date"),
            bio=data.get("bio"),
            remote_ids=str(data.get("remote_ids", {})),  # Convert dict to string
            alternate_names=", ".join(data.get("alternate_names", [])),
            openlibrary_id=data.get("key", "").split("/")[-1],
            photograph=data.get("photograph")
        )