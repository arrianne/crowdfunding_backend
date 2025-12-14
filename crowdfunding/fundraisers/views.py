from django.shortcuts import render

# Create your views here.

# So this view will let the front-end retrieve a list of all fundraisers, so that it can insert that list into a webpage and display it to the user!

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404
from rest_framework import status, permissions
from .permissions import IsOwnerOrReadOnly, IsSupporterOrReadOnly
from .models import Fundraiser, Pledge
from .serializers import FundraiserSerializer, PledgeSerializer, FundraiserDetailSerializer



#############################################
#Fundraisers
#############################################*

class FundraiserList(APIView):
    """
    LIST: Anyone can view all fundraisers.
    CREATE: Only authenticated users can create a fundraiser.

    When a fundraiser is created, the logged-in user is automatically
    assigned as the owner. This prevents users from creating fundraisers
    on behalf of other accounts.
    """
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request):
        # Public endpoint: retrieve all fundraisers
        fundraisers = Fundraiser.objects.all()

        # Use the detail serializer so related data (e.g. pledges)can be included in the response if needed
        serializer = FundraiserDetailSerializer(fundraisers, many=True)
        return Response(serializer.data)

    def post(self, request):
        # POST requires authentication (enforced by permission_classes)
        serializer = FundraiserSerializer(data=request.data)

        if serializer.is_valid():
            # Force owner to be the logged-in user
            # (prevents client-side faking of ownership)
            fundraiser = serializer.save(owner=request.user)

            return Response(
                FundraiserSerializer(fundraiser).data,
                status=status.HTTP_201_CREATED
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FundraiserDetail(APIView):
    """
    RETRIEVE / UPDATE a single fundraiser.

    - Anyone may view a fundraiser.
    - Only the owner may update it.
    - Object-level permissions enforce ownership checks.
    """
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
        IsOwnerOrReadOnly,
    ]

    def get_object(self, pk):
        try:
            fundraiser = Fundraiser.objects.get(pk=pk)

            # Enforce object-level permissions
            # (only the owner can modify this fundraiser)
            self.check_object_permissions(self.request, fundraiser)

            return fundraiser
        except Fundraiser.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        # Public read access to a single fundraiser
        fundraiser = self.get_object(pk)
        serializer = FundraiserDetailSerializer(fundraiser)
        return Response(serializer.data)

    def put(self, request, pk):
        # Partial update (PATCH-style behaviour via PUT)
        fundraiser = self.get_object(pk)

        serializer = FundraiserDetailSerializer(
            instance=fundraiser,
            data=request.data,
            partial=True
        )

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

#############################################
#Pledges
#############################################*


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.http import Http404

from .models import Pledge
from .serializers import PledgeSerializer
from .permissions import IsSupporterOrReadOnly


class PledgeList(APIView):
    """
    LIST: Anyone can view pledges (read-only).
    CREATE: Only authenticated users can create a pledge.
    
    A logged-in user may choose to make their pledge anonymous,
    but the supporter is always stored internally for accountability.
    """
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request):
        # Public endpoint: return all pledges
        pledges = Pledge.objects.all()
        serializer = PledgeSerializer(pledges, many=True)
        return Response(serializer.data)

    def post(self, request):
        # POST requires authentication (enforced by permission_classes)
        serializer = PledgeSerializer(data=request.data)

        if serializer.is_valid():
            # Force supporter to be the logged-in user
            # (prevents clients from spoofing supporter IDs)
            pledge = serializer.save(supporter=request.user)

            fundraiser = pledge.fundraiser

            # If this pledge causes the fundraiser to reach its goal,
            # automatically close the fundraiser to prevent further pledges
            if fundraiser.is_funded and fundraiser.is_open:
                fundraiser.is_open = False
                fundraiser.save(update_fields=["is_open"])

            # Re-serialize the saved pledge so computed fields
            # (e.g. anonymous supporter display) are correct
            return Response(
                PledgeSerializer(pledge).data,
                status=status.HTTP_201_CREATED
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PledgeDetail(APIView):
    """
    RETRIEVE / UPDATE / DELETE a single pledge.

    - Anyone may view a pledge.
    - Only the pledge supporter may update or delete it.
    - Once a fundraiser is closed or funded, updates are blocked
      at the serializer level.
    """
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
        IsSupporterOrReadOnly,
    ]

    def get_object(self, pk):
        try:
            pledge = Pledge.objects.get(pk=pk)
            # Enforce object-level permissions (owner check)
            self.check_object_permissions(self.request, pledge)
            return pledge
        except Pledge.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        # Public read access to a single pledge
        pledge = self.get_object(pk)
        serializer = PledgeSerializer(pledge)
        return Response(serializer.data)

    def put(self, request, pk):
        # Partial update (PATCH-style behaviour via PUT)
        pledge = self.get_object(pk)

        serializer = PledgeSerializer(
            instance=pledge,
            data=request.data,
            partial=True
        )

        if serializer.is_valid():
            # Explicitly preserve the original supporter
            # even if the client attempts to change it
            serializer.save(supporter=pledge.supporter)
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        # Only the supporter may delete their pledge
        pledge = self.get_object(pk)
        pledge.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
