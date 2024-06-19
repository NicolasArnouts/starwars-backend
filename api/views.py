from django.core.exceptions import ValidationError as DjangoValidationError

from rest_framework import viewsets, status, serializers
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.exceptions import (
    NotFound,
    ValidationError as DRFValidationError,
    PermissionDenied,
)
from rest_framework.permissions import IsAuthenticatedOrReadOnly


from rest_framework_simplejwt.views import TokenObtainPairView
from django_filters.rest_framework import DjangoFilterBackend, FilterSet, CharFilter


from .models import Character, Team
from .serializers import (
    CharacterBasicSerializer,
    CharacterFullSerializer,
    TeamSerializer,
    MyTokenObtainPairSerializer,
)


class CharacterFilter(FilterSet):
    name = CharFilter(field_name="name", lookup_expr="icontains")

    class Meta:
        model = Character
        fields = [
            "name",
            "height",
            "mass",
            "gender",
            "homeworld",
            "species",
            "hairColor",
            "eyeColor",
            "skinColor",
            "born",
            "died",
        ]


class CharacterViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for listing or retrieving Characters.
    """

    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = Character.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_class = CharacterFilter

    def get_serializer_class(self):
        if self.action == "list":
            return CharacterBasicSerializer
        return CharacterFullSerializer

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


class TeamViewSet(viewsets.ModelViewSet):
    """
    A ViewSet for listing, retrieving, creating, and updating teams.
    """

    permission_classes = [IsAuthenticatedOrReadOnly]
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

    def destroy(self, request, *args, **kwargs):
        """
        Delete a team if authorized.
        """
        team = self.get_object()
        print("team: ", team)
        if not request.user.is_staff:
            raise PermissionDenied("You do not have permission to delete this team.")

        team.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

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
