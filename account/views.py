# accounts/views.py

from django.shortcuts import render, get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth.hashers import make_password
from django.db import models  # Add this line for Avg
from .models import CustomUser
from post.models import *
from .serializers import SignUpSerializer, UserSerializer

@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    """Register a new user."""
    data = request.data
    serializer = SignUpSerializer(data=data)

    if serializer.is_valid():
        # Check if the username or email is already in use
        if CustomUser.objects.filter(username=data['username']).exists():
            return Response({'detail': 'This username is already taken!'}, status=status.HTTP_400_BAD_REQUEST)
        if CustomUser.objects.filter(email=data['email']).exists():
            return Response({'detail': 'This email is already in use!'}, status=status.HTTP_400_BAD_REQUEST)

        # Create a new user via the serializer
        user = serializer.save()
        return Response({'detail': 'Your account has been successfully registered!'}, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_user(request):
    user = request.user
    user_id = request.data.get('user_id')  # ID of the user to delete (optional)

    try:
        if user.role == 'admin' and user_id:
            # Admin deletes another user
            target_user = CustomUser.objects.get(id=user_id)
            if target_user == user:
                return Response({"error": "Admin cannot delete themselves via this endpoint"},
                              status=status.HTTP_403_FORBIDDEN)
            target_user.delete()
            return Response({"message": f"User {target_user.email} deleted by admin"},
                          status=status.HTTP_204_NO_CONTENT)
        else:
            # User deletes their own account
            if user_id and user_id != str(user.id):
                return Response({"error": "You can only delete your own account"},
                              status=status.HTTP_403_FORBIDDEN)
            user.delete()
            return Response({"message": "Your account has been successfully deleted"},
                          status=status.HTTP_204_NO_CONTENT)
    except CustomUser.DoesNotExist:
        return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def current_user(request):
    """Retrieve the details of the logged-in user."""
    user = request.user
    serializer = UserSerializer(user, many=False)
    return Response(serializer.data)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_user(request):
    """Update the details of the logged-in user."""
    user = request.user
    data = request.data

    # Update basic fields
    user.username = data.get('username', user.username) 
    user.first_name = data.get('first_name', user.first_name)
    user.last_name = data.get('last_name', user.last_name)
    user.email = data.get('email', user.email)

    # Update password if provided
    if data.get('password'):
        user.password = make_password(data['password'])

    # Update employer-specific fields
    if user.role == 'employer':
        user.company_name = data.get('company_name', user.company_name)
        user.company_address = data.get('company_address', user.company_address)
        user.company_website = data.get('company_website', user.company_website)

    # Save the updated user
    user.save()

    # Serialize and return the updated data
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
        total_interview_responses = Interview.objects.count()
        average_score = Interview.objects.aggregate(models.Avg('score'))['score__avg'] or 0.0
        average_salary = Post.objects.aggregate(models.Avg('salaire'))['salaire__avg'] or 0.0
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
            "posts": {"total": total_posts, "average_salary": round(average_salary, 2)},
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
        interview_responses = Interview.objects.filter(user=user)
        response_data = [
            {
                "id": response.id,
                "post_title": response.post.title if hasattr(response, 'post') else "Not linked",
                "question": response.questions,
                "answer": response.responses,
                "score": response.score,
                "final_date": response.end_date,
            }
            for response in interview_responses
        ]
        applications = PostApplication.objects.filter(user=user)
        application_data = [
            {
                "application_id": app.id,  
                "post_title": app.post.title,
                "post_id": app.post.id,
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
                "salary": str(post.salaire),
                "uploaded_at": post.uploaded_at,
                "final_date": post.final_date,
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
                "post_id": app.post.id,
                "interview_id": app.interview.id if app.interview else None,
                "application_date": app.application_date,
                "status": app.status,
                "test": {
                    "question": app.interview.questions if app.interview else None,
                    "answer": app.interview.responses if app.interview else None,
                    "score": app.interview.score if app.interview else None
                } if app.interview else None 
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
        return Response({"error": "Unrecognized role"}, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def verify_user(request, user_id):
    """Allows an admin to verify a user (verified=True)."""
    if not request.user.is_superuser:
        return Response({"error": "Only an admin can verify a user"}, status=status.HTTP_403_FORBIDDEN)

    user_to_verify = get_object_or_404(CustomUser, id=user_id)
    if user_to_verify.verified:
        return Response({"message": f"User {user_to_verify.email} is already verified"}, status=status.HTTP_400_BAD_REQUEST)

    user_to_verify.verified = True
    user_to_verify.save()
    serializer = UserSerializer(user_to_verify, many=False)
    return Response({
        "message": f"User {user_to_verify.email} has been successfully verified",
        "user": serializer.data
    }, status=status.HTTP_200_OK)