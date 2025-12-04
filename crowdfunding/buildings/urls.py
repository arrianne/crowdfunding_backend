from django.urls import path
from . import views

urlpatterns = [
    # List + create buildings
    path('buildings/', views.BuildingList.as_view(), name='building-list'),

    # Single building
    path('buildings/<int:pk>/', views.BuildingDetail.as_view(), name='building-detail'),

    # Fundraisers for a building
    path('buildings/<int:pk>/fundraisers/', views.BuildingFundraisersList.as_view(),
         name='building-fundraisers'),

    # Membership list + create (per building)
    path('buildings/<int:pk>/memberships/', views.BuildingMembershipListCreate.as_view(),
         name='building-memberships'),

    # Single membership
    path('memberships/<int:pk>/', views.BuildingMembershipDetail.as_view(),
         name='membership-detail'),

    # My buildings
    path('my-buildings/', views.MyBuildingsList.as_view(), name='my-buildings'),
]
