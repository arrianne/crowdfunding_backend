from django.shortcuts import render

# Create your views here.

# So this view will let the front-end retrieve a list of all fundraisers, so that it can insert that list into a webpage and display it to the user!

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404
from rest_framework import status, permissions
from .models import Fundraiser, Pledge
from .serializers import FundraiserSerializer, PledgeSerializer, FundraiserDetailSerializer

class FundraiserList(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    # defines the behaviour we want our view to execute when it receives an HTTP GET request.
    def get(self, request):
        # use the Fundraiser model to get a list of all fundraisers in the database
        fundraisers = Fundraiser.objects.all()
        # use the FundraiserSerializer to convert that list to JSON
        serializer = FundraiserDetailSerializer(fundraisers, many=True)
        # return a response containing the serialized data.
        return Response(serializer.data)

    def post(self, request):
        # use the serializer to convert it to a Fundraiser model instance.
        serializer = FundraiserSerializer(data=request.data)
        # We check that the data we got was able to create a valid Fundraiser instance
        if serializer.is_valid():
            serializer.save(owner=request.user)
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
        )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
    )
class FundraiserDetail(APIView):

    def get_object(self, pk):
        try:
            fundraiser = Fundraiser.objects.get(pk=pk)
            return fundraiser
        except Fundraiser.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        fundraiser = self.get_object(pk)
        serializer = FundraiserDetailSerializer(fundraiser)
        return Response(serializer.data)

class PledgeList(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    def get(self, request):
        pledges = Pledge.objects.all()
        serializer = PledgeSerializer(pledges, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = PledgeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(supporter=request.user)
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
    
