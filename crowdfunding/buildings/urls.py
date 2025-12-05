from django.urls import path
from . import views

urlpatterns = [
    path('buildings/', views.BuildingList.as_view(), name='building-list'),
    path('buildings/<int:pk>/', views.BuildingDetail.as_view(), name='building-detail'),
    path('buildings/<int:pk>/fundraisers/', views.BuildingFundraisersList.as_view(),
         name='building-fundraisers'),
]
