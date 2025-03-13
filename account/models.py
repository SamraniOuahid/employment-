# accounts/models.py

from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    """Modèle personnalisé pour les utilisateurs."""
    ROLE_CHOICES = [
        ('employee', 'Employee'),
        ('employer', 'Employer'),
        ('admin', 'Admin'),
    ]

    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='employee', help_text="Role of the user")
    verified = models.BooleanField(default=False, help_text="Indicates if the user is verified")

    # Champs spécifiques aux employeurs
    company_name = models.CharField(max_length=255, blank=True, null=True, help_text="Company name (for employers)")
    company_address = models.CharField(max_length=255, blank=True, null=True, help_text="Company address (for employers)")
    company_website = models.URLField(blank=True, null=True, help_text="Company website (for employers)")

    def __str__(self):
        return self.username