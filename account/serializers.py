# account/serializers.py
from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import CustomUser

class SignUpSerializer(serializers.ModelSerializer):
    """Serializer for user registration with email as the primary identifier."""
    username = serializers.CharField(required=True, allow_blank=False)  
    password = serializers.CharField(write_only=True, min_length=4)

    class Meta:
        model = CustomUser
        fields = (
            'username', 'first_name', 'last_name', 'email', 'password', 'role', 'verified',
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
        """Creates a new user with a hashed password, using the provided username."""
        try:
            validate_password(validated_data['password'])
        except ValidationError as e:
            raise serializers.ValidationError({'password': e.messages})

        # Set is_superuser to True if role is 'admin'
        is_superuser = validated_data['role'] == 'admin'

        # Extract username from validated_data
        username = validated_data.get('username')

        user = CustomUser.objects.create_user(
            username=username,  # Use the username provided by the client
            email=validated_data['email'],
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
    """Serializer to represent users."""
    class Meta:
        model = CustomUser
        fields = (
            'id', 'username', 'first_name', 'last_name', 'email', 'role', 'verified',
            'company_name', 'company_address', 'company_website'
        )
        read_only_fields = ('id', 'verified')


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """Custom serializer to obtain a JWT token using email."""
    username_field = 'email'  # Redefines the identification field as email

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            user = CustomUser.objects.filter(email=email).first()
            if user and user.check_password(password):
                attrs['user'] = user
                return super().validate(attrs)
            else:
                raise serializers.ValidationError('Incorrect email or password.')
        else:
            raise serializers.ValidationError('Please provide an email and a password.')