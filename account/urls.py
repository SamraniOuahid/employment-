# accounts/urls.py

from django.urls import path
from .views import register, current_user, update_user

urlpatterns = [
    # Inscription d'un nouvel utilisateur
    path('register/', register, name='register'),

    # Récupérer les détails de l'utilisateur connecté
    path('current-user/', current_user, name='current_user'),

    # Mettre à jour les détails de l'utilisateur connecté
    path('update-user/', update_user, name='update_user'),
]