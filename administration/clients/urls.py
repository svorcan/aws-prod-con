from django.urls import path
from .views import (
    about,
    ClientCreateView,
    ClientDetailView,
    ClientDeleteView,
    ClientListView,
    ClientUpdateView
)

urlpatterns = [
    path('', ClientListView.as_view(), name='clients-home'),
    path('add/', ClientCreateView.as_view(), name='clients-create'),
    path('<int:pk>/', ClientDetailView.as_view(), name='clients-detail'),
    path('<int:pk>/update/', ClientUpdateView.as_view(), name='clients-update'),
    path('<int:pk>/delete/', ClientDeleteView.as_view(), name='clients-delete'),
    path('about/', about, name='clients-about')
]
