# buildings/views.py

from rest_framework import generics, permissions
from .models import Building
from .serializers import BuildingSerializer

from fundraisers.models import Fundraiser
from fundraisers.serializers import FundraiserSerializer


class BuildingList(generics.ListCreateAPIView):
    """
    GET: List all buildings (public)
    POST: Create a building (logged-in users only)
    """
    queryset = Building.objects.all()
    serializer_class = BuildingSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class BuildingDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    GET: Retrieve a single building
    PUT/PATCH: Update building (owner only ideally)
    DELETE: Delete building (owner only ideally)
    """
    queryset = Building.objects.all()
    serializer_class = BuildingSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    # (you can add IsOwnerOrReadOnly later)


class BuildingFundraisersList(generics.ListAPIView):
    """
    GET /buildings/<pk>/fundraisers/
    List all fundraisers attached to this building
    """
    serializer_class = FundraiserSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        building_id = self.kwargs['pk']
        return Fundraiser.objects.filter(building_id=building_id)
