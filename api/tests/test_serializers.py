from django.test import TestCase
from api.models import Character, Team
from api.serializers import (
    CharacterBasicSerializer,
    CharacterFullSerializer,
    TeamSerializer,
)


class CharacterBasicSerializerTest(TestCase):
    def setUp(self):
        self.character_attributes = {
            "id": 1,
            "name": "Luke Skywalker",
            "height": 172,
            "mass": 77,
            "affiliations": [],
        }
        self.character = Character.objects.create(**self.character_attributes)
        self.serializer = CharacterBasicSerializer(instance=self.character)

    def test_contains_expected_fields(self):
        data = self.serializer.data
        self.assertEqual(
            set(data.keys()),
            set(["id", "name", "image", "height", "mass", "affiliations"]),
        )

    def test_name_field_content(self):
        data = self.serializer.data
        self.assertEqual(data["name"], self.character_attributes["name"])

    def test_height_field_content(self):
        data = self.serializer.data
        self.assertEqual(data["height"], self.character_attributes["height"])

    def test_mass_field_content(self):
        data = self.serializer.data
        self.assertEqual(data["mass"], self.character_attributes["mass"])


class CharacterFullSerializerTest(TestCase):
    def setUp(self):
        self.character_attributes = {
            "id": 1,
            "name": "Luke Skywalker",
            "height": 172,
            "mass": 77,
            "gender": "male",
            "homeworld": "Tatooine",
            "wiki": "http://starwars.wikia.com/wiki/Luke_Skywalker",
            "image": "http://starwars.wikia.com/wiki/Luke_Skywalker/image.jpg",
            "born": "19BBY",
            "bornLocation": "Polis Massa",
            "died": None,
            "diedLocation": None,
            "species": "Human",
            "hairColor": "Blond",
            "eyeColor": "Blue",
            "skinColor": "Light",
            "cybernetics": "",
            "affiliations": [],
            "masters": [],
            "apprentices": [],
            "formerAffiliations": [],
            "creator": "George Lucas",
            "manufacturer": "",
            "model": "",
            "class_field": "",
            "sensorColor": "",
            "platingColor": "",
            "equipment": [],
            "era": [],
            "kajidic": "",
            "armament": [],
        }
        self.character = Character.objects.create(**self.character_attributes)
        self.serializer = CharacterFullSerializer(instance=self.character)

    def test_contains_expected_fields(self):
        data = self.serializer.data
        self.assertEqual(
            set(data.keys()),
            set(
                [
                    "id",
                    "name",
                    "height",
                    "mass",
                    "gender",
                    "homeworld",
                    "wiki",
                    "image",
                    "born",
                    "bornLocation",
                    "died",
                    "diedLocation",
                    "species",
                    "hairColor",
                    "eyeColor",
                    "skinColor",
                    "cybernetics",
                    "affiliations",
                    "masters",
                    "apprentices",
                    "formerAffiliations",
                    "creator",
                    "manufacturer",
                    "model",
                    "class_field",
                    "sensorColor",
                    "platingColor",
                    "equipment",
                    "era",
                    "kajidic",
                    "armament",
                ]
            ),
        )

    def test_name_field_content(self):
        data = self.serializer.data
        self.assertEqual(data["name"], self.character_attributes["name"])

    def test_gender_field_content(self):
        data = self.serializer.data
        self.assertEqual(data["gender"], self.character_attributes["gender"])

    def test_species_field_content(self):
        data = self.serializer.data
        self.assertEqual(data["species"], self.character_attributes["species"])

    def test_born_field_content(self):
        data = self.serializer.data
        self.assertEqual(data["born"], self.character_attributes["born"])

    def test_affiliations_field_content(self):
        data = self.serializer.data
        self.assertEqual(
            data["affiliations"], self.character_attributes["affiliations"]
        )


class TeamSerializerTest(TestCase):
    def setUp(self):
        self.team = Team.objects.create()
        self.character = Character.objects.create(
            id=1,
            name="Luke Skywalker",
            height=172,
            mass=77,
            gender="male",
            homeworld="Tatooine",
        )
        self.team.members.add(self.character)
        self.serializer = TeamSerializer(instance=self.team)

    def test_contains_expected_fields(self):
        data = self.serializer.data
        self.assertEqual(set(data.keys()), set(["id", "members"]))

    def test_members_field_content(self):
        data = self.serializer.data
        self.assertEqual(len(data["members"]), 1)
        self.assertEqual(data["members"][0]["name"], "Luke Skywalker")
