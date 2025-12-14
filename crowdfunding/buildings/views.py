from rest_framework import generics, permissions

from .models import Building
from .serializers import BuildingSerializer

from fundraisers.models import Fundraiser
from fundraisers.serializers import FundraiserSerializer
from fundraisers.permissions import IsOwnerOrReadOnly


class BuildingList(generics.ListCreateAPIView):
    """
    LIST: Anyone can view all buildings.
    CREATE: Only authenticated users can create a building.

    When a building is created, the logged-in user is automatically
    assigned as the owner. This prevents users from creating buildings
    on behalf of other accounts.
    """
    queryset = Building.objects.all()
    serializer_class = BuildingSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        # Force ownership to the logged-in user
        # (prevents client-side spoofing of owner IDs)
        serializer.save(owner=self.request.user)


class BuildingDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    RETRIEVE / UPDATE / DELETE a single building.

    - Anyone may view a building.
    - Only the owner may update or delete it.
    - Object-level permissions enforce ownership checks.
    - Deleting a building will also delete all associated fundraisers
      and pledges via database cascade (on_delete=CASCADE).
    """
    queryset = Building.objects.all()
    serializer_class = BuildingSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
        IsOwnerOrReadOnly,
    ]

class BuildingFundraisersList(generics.ListAPIView):
    """
    LIST all fundraisers associated with a specific building.

    URL pattern:
        /buildings/<pk>/fundraisers/

    This endpoint allows users to view all fundraisers
    belonging to a single building.
    """
    serializer_class = FundraiserSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        # Filter fundraisers by the building ID
        # passed in via the URL (<pk>)
        return Fundraiser.objects.filter(building_id=self.kwargs["pk"])
