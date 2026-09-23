from Database import models

def get_presentationlist(presentations: list[models.Presentation]):
    presentationks = []

    for present in presentations:
        presentationks.append({
            "id": present.id,
            "title": present.name,
            "authors": present.author,
            "description": present.description,
            "cover": None
        })

    return presentationks
    