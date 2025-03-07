from model.Author import Author


class AuthorFactory():

    @staticmethod
    def create_from_json(author_json: str) -> Author:
        personal_name = author_json.get("personal_name")
        try:
            open_library_key = author_json.get("key").split("/")[-1]
        except Exception:
            raise Exception("author's key must not be null")
        birth_date = author_json.get("birth_date")
        if isinstance(author_json.get("bio"), dict):
            bio = author_json.get("bio").get("value")
        else:
            bio = author_json.get("bio")
        fuller_name = author_json.get("fuller_name")
        name = author_json.get("name")

        new_author = Author(
            personal_name=personal_name,
            name=name,
            open_library_key=open_library_key,
            birth_date=birth_date,
            bio=bio,
            fuller_name=fuller_name
        )
        return new_author
