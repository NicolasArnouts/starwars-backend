from django.db import models
from django.core.exceptions import ValidationError


class Character(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    height = models.FloatField(null=True, blank=True)
    mass = models.FloatField(null=True, blank=True)
    gender = models.CharField(max_length=50, null=True, blank=True)
    homeworld = models.CharField(max_length=100, null=True, blank=True)
    wiki = models.URLField(null=True, blank=True)
    image = models.URLField(null=True, blank=True)
    born = models.CharField(max_length=100, null=True, blank=True)
    bornLocation = models.CharField(max_length=100, null=True, blank=True)
    died = models.IntegerField(null=True, blank=True)
    diedLocation = models.CharField(max_length=100, null=True, blank=True)
    species = models.CharField(max_length=50, null=True, blank=True)
    hairColor = models.CharField(max_length=50, null=True, blank=True)
    eyeColor = models.CharField(max_length=50, null=True, blank=True)
    skinColor = models.CharField(max_length=50, null=True, blank=True)
    cybernetics = models.CharField(max_length=255, null=True, blank=True)
    affiliations = models.JSONField(null=True, blank=True)
    masters = models.JSONField(null=True, blank=True)
    apprentices = models.JSONField(null=True, blank=True)
    formerAffiliations = models.JSONField(null=True, blank=True)
    creator = models.CharField(max_length=100, null=True, blank=True)
    manufacturer = models.CharField(max_length=100, null=True, blank=True)
    model = models.CharField(max_length=100, null=True, blank=True)
    class_field = models.CharField(max_length=100, null=True, blank=True)
    sensorColor = models.CharField(max_length=50, null=True, blank=True)
    platingColor = models.CharField(max_length=50, null=True, blank=True)
    equipment = models.JSONField(null=True, blank=True)
    era = models.JSONField(null=True, blank=True)
    kajidic = models.CharField(max_length=100, null=True, blank=True)
    armament = models.JSONField(null=True, blank=True)

    class Meta:
        ordering = ["id"]

    def is_evil(self):
        if "Darth" in self.name or "Sith" in self.name:
            return True
        if self.affiliations and any(
            "Darth" in aff or "Sith" in aff for aff in self.affiliations
        ):
            return True
        if self.masters and any("Darth" in master for master in self.masters):
            return True
        return False


class Team(models.Model):
    members = models.ManyToManyField(Character, blank=True)

    class Meta:
        ordering = ["id"]

    def add_member(self, character):
        if self.members.count() >= 5:
            raise ValidationError("Cannot add member: Team already has 5 members.")
        if character.is_evil():
            raise ValidationError("Cannot add member: Character is considered evil.")
        if self.members.filter(id=character.id).exists():
            raise ValidationError(
                "Cannot add member: Character is already in the team."
            )
        self.members.add(character)

    def remove_member(self, character):
        if character in self.members.all():
            self.members.remove(character)
            return f"{character.name} removed from the team."
        else:
            raise ValidationError("Cannot remove member: Character is not in the team.")
