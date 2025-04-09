# accounts/views.py

from django.shortcuts import render, get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.hashers import make_password
from django.db import models  # Ajoutez cette ligne pour Avg
from .models import CustomUser
from post.models import *
from .serializers import SignUpSerializer, UserSerializer

@api_view(['POST'])
def register(request):
    """Inscription d'un nouvel utilisateur."""
    data = request.data
    serializer = SignUpSerializer(data=data)

    if serializer.is_valid():
        # Vérifier si l'username ou l'email est déjà utilisé
        if CustomUser.objects.filter(username=data['username']).exists():
            return Response({'detail': 'Ce nom d’utilisateur est déjà pris !'}, status=status.HTTP_400_BAD_REQUEST)
        if CustomUser.objects.filter(email=data['email']).exists():
            return Response({'detail': 'Cet email est déjà utilisé !'}, status=status.HTTP_400_BAD_REQUEST)

        # Créer un nouvel utilisateur via le sérializer
        user = serializer.save()
        return Response({'detail': 'Votre compte a été enregistré avec succès !'}, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_user(request):
    user = request.user
    user_id = request.data.get('user_id')  # ID de l'utilisateur à supprimer (optionnel)

    try:
        if user.role == 'admin' and user_id:
            # Admin supprime un autre utilisateur
            target_user = CustomUser.objects.get(id=user_id)
            if target_user == user:
                return Response({"error": "L'admin ne peut pas se supprimer lui-même via cet endpoint"},
                              status=status.HTTP_403_FORBIDDEN)
            target_user.delete()
            return Response({"message": f"Utilisateur {target_user.email} supprimé par l'admin"},
                          status=status.HTTP_204_NO_CONTENT)
        else:
            # Utilisateur supprime son propre compte
            if user_id and user_id != str(user.id):
                return Response({"error": "Vous ne pouvez supprimer que votre propre compte"},
                              status=status.HTTP_403_FORBIDDEN)
            user.delete()
            return Response({"message": "Votre compte a été supprimé avec succès"},
                          status=status.HTTP_204_NO_CONTENT)
    except CustomUser.DoesNotExist:
        return Response({"error": "Utilisateur non trouvé"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    


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
    user = request.user
    role = user.role

    if user.is_superuser:  # Admin
        total_users = CustomUser.objects.count()
        total_posts = Post.objects.count()
        total_cvs = PDFDocument.objects.count()
        total_interview_responses = InterviewResponse.objects.count()
        average_score = InterviewResponse.objects.aggregate(models.Avg('score'))['score__avg'] or 0.0
        average_salaire = Post.objects.aggregate(models.Avg('salaire'))['salaire__avg'] or 0.0
        total_applications = PostApplication.objects.count()
        pending_applications = PostApplication.objects.filter(status='en_attente').count()
        accepted_applications = PostApplication.objects.filter(status='accepte').count()
        total_reports = Report.objects.count()
        reports_data = [
            {
                "id": report.id,
                "post_title": report.post.title,
                "user_email": report.user.email,
                "description": report.description,
                "reported_at": report.reported_at
            }
            for report in Report.objects.all()
        ]
        users_list = [
            {
                "id": u.id,
                "username": u.username,
                "email": u.email,
                "role": u.role,
                "verified": u.verified,
            } for u in CustomUser.objects.all()
        ]

        stats = {
            "users": {"total": total_users, "list": users_list},
            "posts": {"total": total_posts, "average_salaire": round(average_salaire, 2)},
            "cvs": {"total": total_cvs},
            "interview_responses": {"total": total_interview_responses, "average_score": round(average_score, 2)},
            "applications": {
                "total": total_applications,
                "pending": pending_applications,
                "accepted": accepted_applications
            },
            "reports": {
                "total": total_reports,
                "details": reports_data
            }
        }
        return Response(stats, status=status.HTTP_200_OK)

    elif role == 'employee':
        interview_responses = InterviewResponse.objects.filter(user=user)
        response_data = [
            {
                "id": response.id,
                "post_title": response.post.title if hasattr(response, 'post') else "Non lié",
                "question": response.question,
                "answer": response.answer,
                "score": response.score,
                "response_date": response.timestamp
            }
            for response in interview_responses
        ]
        applications = PostApplication.objects.filter(user=user)
        application_data = [
            {
                "post_title": app.post.title,
                "cv_id": app.cv.id if app.cv else None,
                "interview_id": app.interview.id if app.interview else None,
                "status": app.status,
                "application_date": app.application_date
            }
            for app in applications
        ]
        stats = {
            "interview_history": response_data,
            "total_responses": interview_responses.count(),
            "average_score": interview_responses.aggregate(models.Avg('score'))['score__avg'] or 0.0,
            "applications": application_data
        }
        return Response(stats, status=status.HTTP_200_OK)

    elif role == 'employer':
        employer_posts = Post.objects.filter(user=user)
        post_data = [
            {
                "id": post.id,
                "title": post.title,
                "salaire": str(post.salaire),
                "uploaded_at": post.uploaded_at
            }
            for post in employer_posts
        ]
        applications = PostApplication.objects.filter(post__user=user)
        application_data = [
            {
                "id": app.id,
                "post_title": app.post.title,
                "applicant_email": app.user.email,
                "cv_id": app.cv.id if app.cv else None,
                "interview_id": app.interview.id if app.interview else None,
                "application_date": app.application_date,
                "status": app.status,
                "test": {
                    "question": app.interview.question if app.interview else None,
                    "answer": app.interview.answer if app.interview else None,
                    "score": app.interview.score if app.interview else None
                } if app.interview else None  # Ajout du champ test
            }
            for app in applications
        ]
        stats = {
            "my_posts": post_data,
            "total_posts": employer_posts.count(),
            "applications": application_data,
            "total_applications": applications.count(),
            "pending_applications": applications.filter(status='en_attente').count()
        }
        return Response(stats, status=status.HTTP_200_OK)

    else:
        return Response({"error": "Rôle non reconnu"}, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def verify_user(request, user_id):
    """Permet à un admin de valider un utilisateur (verified=True)."""
    if not request.user.is_superuser:
        return Response({"error": "Seul un admin peut valider un utilisateur"}, status=status.HTTP_403_FORBIDDEN)

    user_to_verify = get_object_or_404(CustomUser, id=user_id)
    if user_to_verify.verified:
        return Response({"message": f"L'utilisateur {user_to_verify.email} est déjà vérifié"}, status=status.HTTP_400_BAD_REQUEST)

    user_to_verify.verified = True
    user_to_verify.save()
    serializer = UserSerializer(user_to_verify, many=False)
    return Response({
        "message": f"L'utilisateur {user_to_verify.email} a été vérifié avec succès",
        "user": serializer.data
    }, status=status.HTTP_200_OK)