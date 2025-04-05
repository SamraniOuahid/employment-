# accounts/views.py

from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.hashers import make_password
from django.db import models  # Ajoutez cette ligne pour Avg
from .models import CustomUser
from post.models import Post, PDFDocument, InterviewResponse
from .serializers import SignUpSerializer, UserSerializer

@api_view(['POST'])
def register(request):
    """Inscription d'un nouvel utilisateur."""
    data = request.data
    serializer = SignUpSerializer(data=data)

    if serializer.is_valid():
        # Vérifier si l'email est déjà utilisé
        if CustomUser.objects.filter(email=data['email']).exists():
            return Response({'detail': 'This email already exists!'}, status=status.HTTP_400_BAD_REQUEST)

        # Créer un nouvel utilisateur via le sérializer
        user = serializer.save()
        return Response({'detail': 'Your account has been registered successfully!'}, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def current_user(request):
    """Récupérer les détails de l'utilisateur connecté."""
    user = request.user
    serializer = UserSerializer(user, many=False)
    return Response(serializer.data)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_user(request):
    """Mettre à jour les détails de l'utilisateur connecté."""
    user = request.user
    data = request.data

    # Mettre à jour les champs de base
    user.first_name = data.get('first_name', user.first_name)
    user.last_name = data.get('last_name', user.last_name)
    user.email = data.get('email', user.email)

    # Mettre à jour le mot de passe si fourni
    if data.get('password'):
        user.password = make_password(data['password'])

    # Mettre à jour les champs spécifiques aux employeurs
    if user.role == 'employer':
        user.company_name = data.get('company_name', user.company_name)
        user.company_address = data.get('company_address', user.company_address)
        user.company_website = data.get('company_website', user.company_website)

    # Sauvegarder l'utilisateur mis à jour
    user.save()

    # Sérialiser et retourner les données mises à jour
    serializer = UserSerializer(user, many=False)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def dashboard_stats(request):
    """Récupérer les statistiques du tableau de bord."""
    # Nombre total d'utilisateurs
    total_users = CustomUser.objects.count()
    
    # Répartition par rôle
    employees = CustomUser.objects.filter(role='employee').count()
    employers = CustomUser.objects.filter(role='employer').count()
    admins = CustomUser.objects.filter(role='admin').count()
    
    # Nombre d'utilisateurs vérifiés
    verified_users = CustomUser.objects.filter(verified=True).count()
    
    # Statistiques des posts
    total_posts = Post.objects.count()
    active_posts = Post.objects.filter(final_date__gte='2025-03-22').count()  # Posts actifs (date finale >= aujourd'hui)
    accepted_posts = Post.objects.filter(accepted=True).count()
    
    # Statistiques des CVs (PDFDocument au lieu de PDFUpload)
    total_cvs = PDFDocument.objects.count()
    
    # Statistiques des réponses d’entretien
    total_interview_responses = InterviewResponse.objects.count()
    approved_responses = InterviewResponse.objects.filter(approved=True).count()
    average_score = InterviewResponse.objects.aggregate(models.Avg('score'))['score__avg'] or 0.0
    
    # Statistiques des notifications
    total_notifications = Notification.objects.count()
    unread_notifications = Notification.objects.filter(read=False).count()
    
    # Préparer les données pour la réponse
    stats = {
        "users": {
            "total": total_users,
            "employees": employees,
            "employers": employers,
            "admins": admins,
            "verified": verified_users
        },
        "posts": {
            "total": total_posts,
            "active": active_posts,
            "accepted": accepted_posts
        },
        "cvs": {
            "total": total_cvs
        },
        "interview_responses": {
            "total": total_interview_responses,
            "approved": approved_responses,
            "average_score": round(average_score, 2)
        },
        "notifications": {
            "total": total_notifications,
            "unread": unread_notifications
        }
    }
    
    return Response(stats, status=status.HTTP_200_OK)