from django.contrib.auth import authenticate

from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import Character, Team


class CharacterSerializer(serializers.ModelSerializer):
    """
    Serializer for Character model.
    """

    class Meta:
        model = Character
        fields = "__all__"


class TeamSerializer(serializers.ModelSerializer):
    """
    Serializer for Team model.
    """

    members = CharacterSerializer(many=True, read_only=True)

    class Meta:
        model = Team
        fields = "__all__"


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)

    def validate(self, attrs):
        username = attrs.get("username")
        password = attrs.get("password")

        if username and password:
            user = authenticate(
                request=self.context.get("request"),
                username=username,
                password=password,
            )
            if not user:
                raise serializers.ValidationError("Invalid username or password.")
            attrs["user"] = user

        return super().validate(attrs)

    def get_token(cls, user):
        token = super().get_token(user)
        # Add custom claims
        token["username"] = user.username
        return token
    