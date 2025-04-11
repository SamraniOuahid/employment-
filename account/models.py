# accounts/models.py

from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    username = models.CharField(max_length=150, blank=True, null=True)  # Rendre username facultatif
    email = models.EmailField(unique=True)  # Email unique et obligatoire
    role = models.CharField(max_length=20, choices=[('employee', 'Employee'), ('employer', 'Employer'), ('admin', 'Admin')], default='employee')
    verified = models.BooleanField(default=False)
    company_name = models.CharField(max_length=255, blank=True, null=True)
    company_address = models.CharField(max_length=255, blank=True, null=True)
    company_website = models.URLField(blank=True, null=True)

    USERNAME_FIELD = 'email'  # Définit email comme champ d'identification
    REQUIRED_FIELDS = ['first_name', 'last_name']  # Champs requis lors de la création via createsuperuser

    def __str__(self):
        return self.email