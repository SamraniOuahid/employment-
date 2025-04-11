# account/serializers.py
from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import CustomUser

class SignUpSerializer(serializers.ModelSerializer):
    """Sérializer pour l'inscription des utilisateurs avec email comme identifiant principal."""
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
            'company_name': {'required': False},
            'company_address': {'required': False},
            'company_website': {'required': False},
        }

    def create(self, validated_data):
        """Crée un nouvel utilisateur avec un mot de passe haché, sans username."""
        try:
            validate_password(validated_data['password'])
        except ValidationError as e:
            raise serializers.ValidationError({'password': e.messages})

        # Définir is_superuser à True si role est 'admin'
        is_superuser = validated_data['role'] == 'admin'

        # Si username est requis par le modèle, générer un par défaut basé sur l'email
        email = validated_data['email']

        user = CustomUser.objects.create_user(
            username=username,  # Fournir un username par défaut si nécessaire
            email=email,
            password=validated_data['password'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            role=validated_data['role'],
            verified=validated_data.get('verified', False),
            company_name=validated_data.get('company_name', None),
            company_address=validated_data.get('company_address', None),
            company_website=validated_data.get('company_website', None),
            is_superuser=is_superuser,
            is_staff=is_superuser
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


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """Sérializer personnalisé pour obtenir un token JWT avec email."""
    username_field = 'email'  # Redéfinit le champ d'identification comme email

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            user = CustomUser.objects.filter(email=email).first()
            if user and user.check_password(password):
                attrs['user'] = user
                return super().validate(attrs)
            else:
                raise serializers.ValidationError('Email ou mot de passe incorrect.')
        else:
            raise serializers.ValidationError('Veuillez fournir un email et un mot de passe.')