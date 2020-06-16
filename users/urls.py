from django.urls import path
from .views import profile, dashboard


urlpatterns = [
    path('user-profile/', profile, name='profile'),
    path('user-dashboard/', dashboard, name='dashboard'),
]