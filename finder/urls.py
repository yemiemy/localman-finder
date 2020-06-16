from django.urls import path
from .views import (
    search, 
    PlaceListView, 
    UserPlaceListView, 
    CategoryList, 
    feedback, 
    PlaceDetailView, ListingView, PlaceCreateView,
    PlaceUpdateView,
    PlaceDeleteView,
    about,
    contact
    )


urlpatterns = [
    #path('', index, name='index'),
    path('', PlaceListView.as_view(), name='index'),
    path('listings/', ListingView.as_view(), name='list'),
    path('user/places/<str:username>/', UserPlaceListView.as_view(), name='user-places'),
    path('listings/place/<int:pk>-<str:slug>/', PlaceDetailView.as_view(), name='place-list'),
    path('listings/place/<int:pk>-<str:slug>/delete/', PlaceDeleteView.as_view(), name='place-delete'),
    path('listings/place/<int:pk>-<str:slug>/update/', PlaceUpdateView.as_view(), name='place-update'),
    path('place/new/', PlaceCreateView.as_view(), name='place-create'),
    path('places/category/<str:name>/', CategoryList.as_view(), name='category-list'),
    path('search/', search, name='search'),
    path('feedback/', feedback, name='feedback'),
    path('about/', about, name='about'),
    path('contact-us/', contact, name='contact'),
]