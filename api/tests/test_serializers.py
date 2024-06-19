from django.test import TestCase
from api.models import Character, Team
from api.serializers import CharacterSerializer, TeamSerializer


class CharacterSerializerTest(TestCase):
    def setUp(self):
        self.character_attributes = {
            "id": 1,
            "name": "Luke Skywalker",
            "height": 172,
            "mass": 77,
            "affiliations": [],
        }
        self.character = Character.objects.create(**self.character_attributes)
        self.serializer = CharacterSerializer(instance=self.character)

    def test_contains_expected_fields(self):
        data = self.serializer.data
        self.assertEqual(
            set(data.keys()),
            set(["id", "name", "image", "height", "mass", "affiliations"]),
        )

    def test_name_field_content(self):
        data = self.serializer.data
        self.assertEqual(data["name"], self.character_attributes["name"])


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
