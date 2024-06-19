from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from api.models import Character, Team
from django.contrib.auth.models import User


class CharacterViewSetTest(APITestCase):
    def setUp(self):
        # Clean up the database
        Character.objects.all().delete()

        # Create user and try to log in
        self.user = User.objects.create_user(username="testuser", password="testpass")
        login_successful = self.client.login(username="testuser", password="testpass")

        # # Debug statements
        # if not login_successful:
        #     print("Login failed")
        # else:
        #     print("Login successfull")

        self.character = Character.objects.create(
            id=1,
            name="Luke Skywalker",
            height=172,
            mass=77,
            gender="male",
            homeworld="Tatooine",
        )
        self.evil_character = Character.objects.create(
            id=2, name="Darth Vader", affiliations=["Sith"]
        )

    def test_list_characters(self):
        url = reverse("character-list")
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(int(response.data["count"]), 2)

    def test_retrieve_character(self):
        url = reverse("character-detail", args=[self.character.id])
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "Luke Skywalker")

    def test_filter_characters(self):
        url = reverse("character-list") + "?name=Luke Skywalker"
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(int(response.data["count"]), 1)
        self.assertEqual(response.data["results"][0]["name"], "Luke Skywalker")


class TeamViewSetTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.admin_user = User.objects.create_superuser(
            username="adminuser", password="adminpass"
        )
        login_successful = self.client.login(username="testuser", password="testpass")
        print(login_successful)

        self.client.login(username="adminuser", password="adminpass")

        self.team = Team.objects.create()
        self.character = Character.objects.create(
            id=1,
            name="Luke Skywalker",
            height=172,
            mass=77,
            gender="male",
            homeworld="Tatooine",
        )
        self.evil_character = Character.objects.create(
            id=2, name="Darth Vader", affiliations=["Sith"]
        )

    def test_delete_team(self):
        url = reverse("team-detail", args=[self.team.id])
        self.client.login(username="adminuser", password="adminpass")
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Team.objects.filter(id=self.team.id).exists())

    def test_delete_team_unauthorized(self):
        url = reverse("team-detail", args=[self.team.id])
        self.client.login(username="testuser", password="testpass")
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_team(self):
        url = reverse("team-list")
        response = self.client.post(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_add_member(self):
        url = reverse("team-add-member", args=[self.team.id])
        response = self.client.post(
            url, {"character_id": self.character.id}, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn(self.character, self.team.members.all())

    def test_add_evil_member(self):
        url = reverse("team-add-member", args=[self.team.id])
        response = self.client.post(
            url, {"character_id": self.evil_character.id}, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_remove_member(self):
        self.team.add_member(self.character)
        url = reverse("team-remove-member", args=[self.team.id])
        response = self.client.post(
            url, {"character_id": self.character.id}, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotIn(self.character, self.team.members.all())

    def test_remove_member_not_in_team(self):
        url = reverse("team-remove-member", args=[self.team.id])
        response = self.client.post(
            url, {"character_id": self.character.id}, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
