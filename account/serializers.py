# accounts/serializers.py

from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from .models import CustomUser

class SignUpSerializer(serializers.ModelSerializer):
    """Sérializer pour l'inscription des utilisateurs."""
    password = serializers.CharField(write_only=True, min_length=4)

    class Meta:
        model = CustomUser
        fields = (
            'first_name', 'last_name', 'email', 'password', 'role', 'verified',
            'company_name', 'company_address', 'company_website'
        )
        extra_kwargs = {
            'first_name': {'required': True, 'allow_blank': False},
            'last_name': {'required': True, 'allow_blank': False},
            'email': {'required': True, 'allow_blank': False},
            'password': {'write_only': True},
            'company_name': {'required': False},  # Optionnel pour les employeurs
            'company_address': {'required': False},  # Optionnel pour les employeurs
            'company_website': {'required': False},  # Optionnel pour les employeurs
        }

    def create(self, validated_data):
        """Crée un nouvel utilisateur avec un mot de passe haché."""
        try:
            validate_password(validated_data['password'])  # Valide le mot de passe
        except ValidationError as e:
            raise serializers.ValidationError({'password': e.messages})

        user = CustomUser.objects.create_user(
            username=validated_data['email'],  # Utilisez l'email comme nom d'utilisateur
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            role=validated_data['role'],
            verified=validated_data.get('verified', False),
            company_name=validated_data.get('company_name', None),
            company_address=validated_data.get('company_address', None),
            company_website=validated_data.get('company_website', None),
        )
        return user


class UserSerializer(serializers.ModelSerializer):
    """Sérializer pour représenter les utilisateurs."""

    class Meta:
        model = CustomUser
        fields = (
            'id', 'first_name', 'last_name', 'email', 'role', 'verified',
            'company_name', 'company_address', 'company_website'
        )
        read_only_fields = ('id', 'verified')