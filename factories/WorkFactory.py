from model.Work import Work

class WorkFactory:
    @staticmethod
    def create_from_json(work_json, authors=None) -> Work:

        title = work_json.get("title", "Unknown Title")
        try:
            open_library_key = work_json.get("key", "").split("/")[-1]  # Extract the key part
        except Exception:
            raise Exception(f"open library key for work '{title}' is null!")

        description = work_json.get("description")
        first_publish_date = work_json.get("first_publish_date", "")
        first_sentence = work_json.get("first_sentence")
        links = work_json.get("links")
        covers = work_json.get("covers")
        subject_places = work_json.get("subject_places")
        subjects = work_json.get("subjects")
        subject_people = work_json.get("subject_people")
        subject_times = work_json.get("subject_times")
        excerpts = work_json.get("excerpts")
        created_at = work_json.get("created_at")
        last_modified = work_json.get("last_modified")

        new_work = Work(
            title=title,
            open_library_key=open_library_key,
            description=description,
            first_publish_date=first_publish_date,
            first_sentence=first_sentence,
            links=links,
            covers=covers,
            subject_places=subject_places,
            subjects=subjects,
            subject_people=subject_people,
            subject_times=subject_times,
            excerpts=excerpts,
            created_at=created_at,
            last_modified=last_modified,
        )
        return new_work
