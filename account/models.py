# account/models.py
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        """Crée et enregistre un utilisateur normal avec un email et un mot de passe."""
        if not email:
            raise ValueError("L'email doit être fourni.")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """Crée et enregistre un superutilisateur avec un email et un mot de passe."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', 'admin')  # Définit le rôle comme 'admin' par défaut
        extra_fields.setdefault('verified', True)  # Superutilisateur vérifié par défaut

        if extra_fields.get('is_staff') is not True:
            raise ValueError("Le superutilisateur doit avoir is_staff=True.")
        if extra_fields.get('is_superuser') is not True:
            raise ValueError("Le superutilisateur doit avoir is_superuser=True.")

        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractUser):
    username = models.CharField(max_length=150, blank=True, null=True)  # Facultatif
    email = models.EmailField(unique=True, blank=False, null=False)  # Obligatoire et unique
    role = models.CharField(max_length=20, choices=[('employee', 'Employee'), ('employer', 'Employer'), ('admin', 'Admin')], default='employee')
    verified = models.BooleanField(default=False)
    company_name = models.CharField(max_length=255, blank=True, null=True)
    company_address = models.CharField(max_length=255, blank=True, null=True)
    company_website = models.URLField(blank=True, null=True)

    USERNAME_FIELD = 'email'  # Identifiant principal
    REQUIRED_FIELDS = ['first_name', 'last_name']  # Champs requis pour createsuperuser

    objects = CustomUserManager()  # Utilise le manager personnalisé

    def __str__(self):
        return self.email