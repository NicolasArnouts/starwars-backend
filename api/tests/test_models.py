from django.test import TestCase
from api.models import Character, Team
from django.core.exceptions import ValidationError


class CharacterModelTest(TestCase):
    def setUp(self):
        self.character = Character.objects.create(
            id=1,
            name="Luke Skywalker",
            height=172,
            mass=77,
            gender="male",
            homeworld="Tatooine",
            affiliations=[],
        )

    def test_character_creation(self):
        self.assertEqual(self.character.name, "Luke Skywalker")
        self.assertEqual(self.character.height, 172)
        self.assertEqual(self.character.mass, 77)

    def test_character_is_evil(self):
        evil_character = Character.objects.create(
            id=2, name="Darth Vader", affiliations=["Sith"]
        )
        self.assertTrue(evil_character.is_evil())

    def test_character_is_not_evil(self):
        self.assertFalse(self.character.is_evil())


class TeamModelTest(TestCase):
    def setUp(self):
        self.team = Team.objects.create()
        self.character = Character.objects.create(
            id=1,
            name="Luke Skywalker",
            height=172,
            mass=77,
            gender="male",
            homeworld="Tatooine",
            affiliations=[],
        )
        self.evil_character = Character.objects.create(
            id=2, name="Darth Vader", affiliations=["Sith"]
        )

    def test_add_member(self):
        self.team.add_member(self.character)
        self.assertIn(self.character, self.team.members.all())

    def test_add_evil_member(self):
        with self.assertRaises(ValidationError):
            self.team.add_member(self.evil_character)

    def test_remove_member(self):
        self.team.add_member(self.character)
        self.team.remove_member(self.character)
        self.assertNotIn(self.character, self.team.members.all())

    def test_add_duplicate_member(self):
        self.team.add_member(self.character)
        with self.assertRaises(ValidationError):
            self.team.add_member(self.character)

    def test_add_member_when_team_is_full(self):
        for i in range(3, 8):  # Start from 3 to avoid ID conflicts
            Character.objects.create(
                id=i,
                name=f"Character {i-2}",
                height=180,
                mass=80,
                gender="male",
                homeworld="Earth",
                affiliations=[],
            )
            self.team.add_member(Character.objects.get(id=i))
        new_character = Character.objects.create(
            id=8,
            name="New Character",
            height=180,
            mass=80,
            gender="male",
            homeworld="Earth",
            affiliations=[],
        )
        with self.assertRaises(ValidationError):
            self.team.add_member(new_character)

    def test_remove_member_not_in_team(self):
        with self.assertRaises(ValidationError):
            self.team.remove_member(self.character)
