from django.urls import path
from . import views

from django.urls import path
from . import views

urlpatterns = [
    path('buildings/', views.BuildingList.as_view(), name='building-list'),
    path('my-buildings/', views.MyBuildingsList.as_view(), name='my-buildings'),
    path('buildings/<int:pk>/', views.BuildingDetail.as_view(), name='building-detail'),
    path('buildings/<int:pk>/fundraisers/', views.BuildingFundraisersList.as_view(),
         name='building-fundraisers'),
    path('buildings/<int:pk>/memberships/', views.BuildingMembershipListCreate.as_view(),
         name='building-memberships'),
]
