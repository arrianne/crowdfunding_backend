from rest_framework import generics, permissions
from .models import Building
from .serializers import BuildingSerializer

from fundraisers.models import Fundraiser
from fundraisers.serializers import FundraiserSerializer


class BuildingList(generics.ListCreateAPIView):
    queryset = Building.objects.all()
    serializer_class = BuildingSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class BuildingDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Building.objects.all()
    serializer_class = BuildingSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class BuildingFundraisersList(generics.ListAPIView):
    serializer_class = FundraiserSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        return Fundraiser.objects.filter(building_id=self.kwargs['pk'])
