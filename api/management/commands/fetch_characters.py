import requests
from django.core.management.base import BaseCommand
from api.models import Character


class Command(BaseCommand):
    help = "Fetch Star Wars characters from the API"

    def handle(self, *args, **kwargs):
        response = requests.get("https://akabab.github.io/starwars-api/api/all.json")
        data = response.json()
        for item in data:
            character, created = Character.objects.update_or_create(
                id=item["id"],
                defaults={
                    "name": item["name"],
                    "height": item.get("height"),
                    "mass": item.get("mass"),
                    "gender": item.get("gender"),
                    "homeworld": item.get("homeworld"),
                    "wiki": item.get("wiki"),
                    "image": item.get("image"),
                    "born": item.get("born"),
                    "bornLocation": item.get("bornLocation"),
                    "died": item.get("died"),
                    "diedLocation": item.get("diedLocation"),
                    "species": item.get("species"),
                    "hairColor": item.get("hairColor"),
                    "eyeColor": item.get("eyeColor"),
                    "skinColor": item.get("skinColor"),
                    "cybernetics": item.get("cybernetics"),
                    "affiliations": item.get("affiliations", []),
                    "masters": item.get("masters", []),
                    "apprentices": item.get("apprentices", []),
                    "formerAffiliations": item.get("formerAffiliations", []),
                    "creator": item.get("creator"),
                    "manufacturer": item.get("manufacturer"),
                    "model": item.get("model"),
                    "class_field": item.get("class"),
                    "sensorColor": item.get("sensorColor"),
                    "platingColor": item.get("platingColor"),
                    "equipment": item.get("equipment", []),
                    "era": item.get("era", []),
                    "kajidic": item.get("kajidic"),
                    "armament": item.get("armament", []),
                },
            )

            if created:
                print(f"Created character: {character.name}")
            else:
                print(f"Updated character: {character.name}")
        print("Finished fetching from API")
