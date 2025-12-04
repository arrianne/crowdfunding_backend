# buildings/views.py

from rest_framework import generics, permissions
from .models import Building, BuildingMembership
from .serializers import (
    BuildingSerializer,
    BuildingMembershipSerializer,
)

from fundraisers.models import Fundraiser
from fundraisers.serializers import FundraiserSerializer


class BuildingList(generics.ListCreateAPIView):
    """
    GET: list all buildings (public)
    POST: create a building (logged-in users only)
    """
    queryset = Building.objects.all()
    serializer_class = BuildingSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        building = serializer.save(owner=self.request.user)

        # Optionally: auto-make creator a committee member
        BuildingMembership.objects.get_or_create(
            user=self.request.user,
            building=building,
            defaults={'role': BuildingMembership.COMMITTEE},
        )


class MyBuildingsList(generics.ListAPIView):
    """
    List buildings where the current user is a member.
    """
    serializer_class = BuildingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Building.objects.filter(
            memberships__user=self.request.user
        ).distinct()


class BuildingFundraisersList(generics.ListAPIView):
    """
    List all fundraisers for a given building.
    GET /buildings/<pk>/fundraisers/
    """
    serializer_class = FundraiserSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        building_id = self.kwargs['pk']
        return Fundraiser.objects.filter(building_id=building_id)
    
class BuildingDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Building.objects.all()
    serializer_class = BuildingSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]



class BuildingMembershipListCreate(generics.ListCreateAPIView):
    """
    GET: list memberships for a building
    POST: add current user as a member of this building
    """
    serializer_class = BuildingMembershipSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        building_id = self.kwargs['pk']
        return BuildingMembership.objects.filter(building_id=building_id)

    def perform_create(self, serializer):
        building_id = self.kwargs['pk']
        serializer.save(
            user=self.request.user,
            building_id=building_id,
        )
