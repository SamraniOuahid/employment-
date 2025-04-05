from django.urls import path
from .views import * # Ajoutez dashboard_stats

urlpatterns = [
    path('register/', register, name='register'),
    path('users/delete/', delete_user, name='delete_user'),
    path('current-user/', current_user, name='current_user'),
    path('update-user/', update_user, name='update_user'),
    path('dashboard-stats/', dashboard_stats, name='dashboard_stats'),  # Nouvel endpoint
]