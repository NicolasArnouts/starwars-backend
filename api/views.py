from django.contrib.auth import authenticate
from rest_framework import viewsets, status, serializers
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.exceptions import NotFound, ValidationError as DRFValidationError
from rest_framework_simplejwt.views import TokenObtainPairView
from django.core.exceptions import ValidationError as DjangoValidationError

from .models import Character, Team
from .serializers import (
    CharacterSerializer,
    TeamSerializer,
    MyTokenObtainPairSerializer,
)


class CharacterViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for listing or retrieving Characters.
    """

    queryset = Character.objects.all()
    serializer_class = CharacterSerializer

    def list(self, request):
        """
        Return a list of all the existing characters.
        """
        try:
            queryset = self.filter_queryset(self.get_queryset())
            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)

            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response(
                {"status": "error", "message": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def retrieve(self, request, *args, **kwargs):
        """
        Retrieve a specific character by ID.
        """
        try:
            character = self.get_object()
            serializer = self.get_serializer(character)
            return Response(serializer.data)
        except Character.DoesNotExist:
            raise NotFound("Character not found")
        except Exception as e:
            return Response(
                {"status": "error", "message": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def get_queryset(self):
        """
        Optionally restricts the returned characters,
        by filtering against a `name` query parameter in the URL.
        """
        try:
            queryset = Character.objects.all()
            name = self.request.query_params.get("name", None)
            if name:
                queryset = queryset.filter(name__icontains=name)
            return queryset
        except Exception as e:
            raise DRFValidationError(f"Invalid query parameter: {e}")


class TeamViewSet(viewsets.ModelViewSet):
    """
    A ViewSet for listing, retrieving, creating, and updating teams.
    """

    queryset = Team.objects.all()
    serializer_class = TeamSerializer

    def create(self, request, *args, **kwargs):
        """
        Create a new team.
        """
        try:
            team = Team.objects.create()
            serializer = self.get_serializer(team)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except DRFValidationError as e:
            return Response(
                {"status": "error", "message": str(e)},
                status=status.HTTP_400_BAD_REQUEST,
            )

    @action(detail=True, methods=["post"])
    def add_member(self, request, pk=None):
        """
        Add a character to the specified team.
        """
        try:
            team = self.get_object()
            character_id = request.data.get("character_id")
            character = Character.objects.get(id=character_id)
            team.add_member(character)
            return Response(
                {"status": "Character added to the team"},
                status=status.HTTP_201_CREATED,
            )
        except Team.DoesNotExist:
            return Response(
                {"status": "error", "message": "Team not found"},
                status=status.HTTP_404_NOT_FOUND,
            )
        except Character.DoesNotExist:
            return Response(
                {"status": "error", "message": "Character not found"},
                status=status.HTTP_404_NOT_FOUND,
            )
        except DjangoValidationError as e:
            return Response(
                {"status": "error", "message": str(e.message)},
                status=status.HTTP_400_BAD_REQUEST,
            )

    @action(detail=True, methods=["post"])
    def remove_member(self, request, pk=None):
        """
        Remove a character from the specified team.
        """
        try:
            team = self.get_object()
            character_id = request.data.get("character_id")
            character = Character.objects.get(id=character_id)
            message = team.remove_member(character)
            return Response(
                {"status": "Character removed from the team", "message": message},
                status=status.HTTP_200_OK,
            )
        except Team.DoesNotExist:
            return Response(
                {"status": "error", "message": "Team not found"},
                status=status.HTTP_404_NOT_FOUND,
            )
        except Character.DoesNotExist:
            return Response(
                {"status": "error", "message": "Character not found"},
                status=status.HTTP_404_NOT_FOUND,
            )
        except DjangoValidationError as e:
            return Response(
                {"status": "error", "message": str(e.message)},
                status=status.HTTP_400_BAD_REQUEST,
            )


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
