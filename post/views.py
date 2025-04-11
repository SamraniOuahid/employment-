from django.shortcuts import render, get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.views import APIView
from .models import *
from .serializers import PostSerializer, PDFDocumentSerializer, EvaluateResponsesSerializer
from .ai_algorithm import compare_cv_with_post
from .utils import extract_text_from_pdf
from .interview_system import generate_questions, evaluate_responses

# Get all posts
@api_view(['GET'])
def get_all_post(request):
    posts = Post.objects.all()
    serializer = PostSerializer(posts, many=True)
    return Response({"posts": serializer.data})

# Get post by ID
@api_view(['GET'])
def get_by_id(request, pk):
    post = get_object_or_404(Post, id=pk)
    serializer = PostSerializer(post, many=False)
    return Response({"post": serializer.data})

# Create a new post
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def new_post(request):
    data = request.data
    serializer = PostSerializer(data=data)
    if serializer.is_valid():
        post = Post.objects.create(**data, user=request.user)
        res = PostSerializer(post, many=False)
        return Response({"post": res.data})
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Update a post
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_post(request, pk):
    post = get_object_or_404(Post, id=pk)
    if post.user != request.user:
        return Response({"error": "Sorry, you cannot update this post"}, status=status.HTTP_403_FORBIDDEN)
    
    post.title = request.data.get('title', post.title)
    post.description = request.data.get('description', post.description)
    post.final_date = request.data.get('final_date', post.final_date)
    post.save()
    serializer = PostSerializer(post, many=False)
    return Response({"post": serializer.data})

# Delete a post
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_post(request, pk):
    post = get_object_or_404(Post, id=pk)
    # Allow the creator OR an admin (superuser)
    if post.user != request.user and not request.user.is_superuser:
        return Response({"error": "Sorry, you cannot delete this post"}, status=status.HTTP_403_FORBIDDEN)
    post.delete()
    return Response({"message": "The post is deleted"}, status=status.HTTP_200_OK)

# Upload a PDF (e.g., CV)
class PDFUploadView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = PDFDocumentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Compare CV with Post
class CompareCVWithPost(APIView):
    def post(self, request, *args, **kwargs):
        cv_id = request.data.get('cv_id')
        post_id = request.data.get('post_id')
        
        try:
            pdf_document = PDFDocument.objects.get(id=cv_id)
            post = Post.objects.get(id=post_id)
        except (PDFDocument.DoesNotExist, Post.DoesNotExist):
            return Response({"error": "CV or post not found."}, status=status.HTTP_404_NOT_FOUND)

        cv_text = extract_text_from_pdf(pdf_document.pdf_file.path)
        similarity_score = compare_cv_with_post(cv_text, post.description)

        # Check if an application already exists
        application, created = PostApplication.objects.get_or_create(
            post=post, user=request.user, cv=pdf_document,
            defaults={'step': 'cv_compared'}
        )
        
        if similarity_score > 0.5:
            application.step = 'cv_compared'
            application.save()
            return Response({
                "message": "Your CV matches the post. Next step: save the interview.",
                "similarity_score": round(similarity_score * 100, 2),
                "application_id": application.id
            })
        else:
            application.status = 'refuse'
            application.save()
            return Response({
                "message": "Sorry, your CV does not match the post.",
                "similarity_score": round(similarity_score * 100, 2)
            })
        

# Generate interview questions
class InterviewView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        # Authentication check (redundant but explicit)
        if not request.user.is_authenticated:
            return Response({"error": "User not authenticated."}, status=status.HTTP_401_UNAUTHORIZED)

        # Retrieve and validate application_id
        application_id = request.data.get('application_id')
        if not application_id:
            return Response({"error": "The application_id is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            application_id = int(application_id)
        except (TypeError, ValueError):
            return Response({"error": "The application_id must be a valid integer."}, status=status.HTTP_400_BAD_REQUEST)

        # Retrieve the application
        try:
            application = PostApplication.objects.get(id=application_id, user=request.user)
            if application.step != 'interview_saved':
                return Response({"error": "The interview must be saved before starting."}, status=status.HTTP_400_BAD_REQUEST)
            
            # Check the interview
            interview = application.interview
            if not interview:
                return Response({"error": "No interview associated."}, status=status.HTTP_400_BAD_REQUEST)

            # Check the post description
            if not application.post.description:
                return Response({"error": "The post description is empty."}, status=status.HTTP_400_BAD_REQUEST)

            # Generate questions
            try:
                questions = generate_questions(application.post.description, num_questions=5)
                if not questions:
                    return Response({"error": "Failed to generate questions."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            except Exception as e:
                return Response({"error": f"Error generating questions: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            # Save questions and update
            interview.questions = questions
            interview.status = 'in_progress'
            interview.save()
            application.step = 'questions_generated'
            application.save()

            return Response({
                "message": "Questions generated. Submit your answers.",
                "questions": questions,
                "interview_id": interview.id
            })
        except PostApplication.DoesNotExist:
            return Response({"error": "Application not found."}, status=status.HTTP_404_NOT_FOUND)

# Submit text responses for interview
class SubmitInterviewResponse(APIView):
    def post(self, request, *args, **kwargs):
        application_id = request.data.get('application_id')
        responses = request.data.get('responses')  # List of responses

        try:
            application = PostApplication.objects.get(id=application_id, user=request.user)
            if application.step != 'questions_generated':
                return Response({"error": "Questions must be generated before submitting answers."}, status=status.HTTP_400_BAD_REQUEST)
            
            interview = application.interview
            if not interview or not interview.questions:
                return Response({"error": "No questions found for this interview."}, status=status.HTTP_400_BAD_REQUEST)

            if len(responses) != len(interview.questions):
                return Response({"error": "The number of responses must match the number of questions."}, status=status.HTTP_400_BAD_REQUEST)

            interview.responses = responses
            interview.save()
            application.step = 'answers_submitted'
            application.save()

            return Response({"message": "Answers submitted. Next step: evaluation."})
        except PostApplication.DoesNotExist:
            return Response({"error": "Application not found."}, status=status.HTTP_404_NOT_FOUND)
        

    
# Evaluate text responses
class EvaluateTextResponsesAPIView(APIView):
    def post(self, request, *args, **kwargs):
        application_id = request.data.get('application_id')
        try:
            application = PostApplication.objects.get(id=application_id, user=request.user)
            if application.step != 'answers_submitted':
                return Response({"error": "Answers must be submitted before evaluation."}, status=status.HTTP_400_BAD_REQUEST)
            
            interview = application.interview
            if not interview.responses:
                return Response({"error": "No responses found for this interview."}, status=status.HTTP_400_BAD_REQUEST)

            final_score, scores = evaluate_responses(interview.responses, application.post.description, interview.questions)
            interview.score = final_score
            interview.status = 'completed'
            interview.save()
            application.step = 'evaluated'
            application.status = 'accepte' if final_score > 70 else 'refuse'
            application.save()

            return Response({
                "message": "Evaluation completed.",
                "final_score": final_score,
                "scores": scores
            })
        except PostApplication.DoesNotExist:
            return Response({"error": "Application not found."}, status=status.HTTP_404_NOT_FOUND)




@api_view(['POST'])
@permission_classes([IsAuthenticated])
def apply_to_post(request):
    post_id = request.data.get('post_id')
    cv_id = request.data.get('cv_id')  # New field

    try:
        post = Post.objects.get(id=post_id)
        cv = PDFDocument.objects.get(id=cv_id, user=request.user) if cv_id else None

        # Check if the user has already applied
        if PostApplication.objects.filter(post=post, user=request.user).exists():
            return Response({"error": "You have already applied for this post"}, status=status.HTTP_400_BAD_REQUEST)

        # Create an application
        application = PostApplication.objects.create(
            post=post,
            user=request.user,
            cv=cv
        )
        return Response({
            "application": {
                "post_id": post.id,
                "user_id": request.user.id,
                "cv_id": cv.id if cv else None,
                "status": application.status,
                "application_date": application.application_date
            }
        }, status=status.HTTP_201_CREATED)
    except Post.DoesNotExist:
        return Response({"error": "Post not found."}, status=status.HTTP_404_NOT_FOUND)
    except PDFDocument.DoesNotExist:
        return Response({"error": "CV not found or unauthorized."}, status=status.HTTP_404_NOT_FOUND)

@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def update_application_status(request):
    application_id = request.data.get('application_id')
    new_status = request.data.get('status')
    interview_id = request.data.get('interview_id')  # New field

    try:
        application = PostApplication.objects.get(id=application_id, post__user=request.user)
        if new_status not in ['accepte', 'refuse', 'en_attente']:
            return Response({"error": "Invalid status."}, status=status.HTTP_400_BAD_REQUEST)

        application.status = new_status
        if interview_id:
            try:
                interview = InterviewResponse.objects.get(id=interview_id, user=application.user)
                application.interview = interview
            except InterviewResponse.DoesNotExist:
                return Response({"error": "Interview not found."}, status=status.HTTP_404_NOT_FOUND)

        application.save()
        return Response({
            "application": {
                "id": application.id,
                "post_id": application.post.id,
                "user_id": application.user.id,
                "cv_id": application.cv.id if application.cv else None,
                "interview_id": application.interview.id if application.interview else None,
                "status": application.status
            }
        }, status=status.HTTP_200_OK)
    except PostApplication.DoesNotExist:
        return Response({"error": "Application not found or unauthorized."}, status=status.HTTP_404_NOT_FOUND)
    





@api_view(['POST'])
@permission_classes([IsAuthenticated])
def report_post(request):
    post_id = request.data.get('post_id')
    description = request.data.get('description')

    if not description:
        return Response({"error": "A description of the issue is required."}, status=status.HTTP_400_BAD_REQUEST)

    try:
        post = Post.objects.get(id=post_id)
        # Check if the user has already reported this post
        if Report.objects.filter(post=post, user=request.user).exists():
            return Response({"error": "You have already reported this post"}, status=status.HTTP_400_BAD_REQUEST)

        report = Report.objects.create(
            post=post,
            user=request.user,
            description=description
        )
        return Response({
            "report": {
                "id": report.id,
                "post_id": post.id,
                "user_id": request.user.id,
                "description": report.description,
                "reported_at": report.reported_at
            }
        }, status=status.HTTP_201_CREATED)
    except Post.DoesNotExist:
        return Response({"error": "Post not found."}, status=status.HTTP_404_NOT_FOUND)
    




@api_view(['GET'])
@permission_classes([IsAuthenticated])
def interview_data(request):
    user = request.user

    if user.is_superuser:  # Admin
        # Retrieve all interview data
        interviews = InterviewResponse.objects.all()
        interview_data = [
            {
                "id": interview.id,
                "post_title": interview.post.title,
                "user_email": interview.user.email,
                "question": interview.question,
                "answer": interview.answer,
                "score": interview.score,
                "timestamp": interview.timestamp
            } for interview in interviews
        ]
        return Response({
            "total_interviews": interviews.count(),
            "interview_data": interview_data
        }, status=status.HTTP_200_OK)

    elif user.role == 'employee':  # Employee
        # Retrieve only interviews of the logged-in user
        interviews = InterviewResponse.objects.filter(user=user)
        interview_data = [
            {
                "id": interview.id,
                "post_title": interview.post.title,
                "question": interview.question,
                "answer": interview.answer,
                "score": interview.score,
                "timestamp": interview.timestamp
            } for interview in interviews
        ]
        return Response({
            "total_interviews": interviews.count(),
            "interview_data": interview_data
        }, status=status.HTTP_200_OK)

    elif user.role == 'employer':  # Employer
        # Retrieve interviews related to posts created by the employer
        interviews = InterviewResponse.objects.filter(post__user=user)
        interview_data = [
            {
                "id": interview.id,
                "post_title": interview.post.title,
                "user_email": interview.user.email,
                "question": interview.question,
                "answer": interview.answer,
                "score": interview.score,
                "timestamp": interview.timestamp
            } for interview in interviews
        ]
        return Response({
            "total_interviews": interviews.count(),
            "interview_data": interview_data
        }, status=status.HTTP_200_OK)

    else:
        return Response({"error": "Unrecognized role."}, status=status.HTTP_400_BAD_REQUEST)
    

class SaveInterview(APIView):
    permission_classes = [IsAuthenticated]  # Ensures that only authenticated users can access

    def post(self, request, *args, **kwargs):
        application_id = request.data.get('application_id')
        try:
            # Verify that the user is authenticated and retrieve the application
            application = PostApplication.objects.get(id=application_id, user=request.user)
            if application.step != 'cv_compared':
                return Response({"error": "You must first pass the CV/Post comparison."}, status=status.HTTP_400_BAD_REQUEST)
            
            # Create the interview
            interview = Interview.objects.create(
                post=application.post,
                user=request.user,  # Authenticated user
                status='planned'
            )
            application.interview = interview
            application.step = 'interview_saved'
            application.save()

            return Response({
                "message": "Interview saved. Click to start.",
                "interview_id": interview.id
            }, status=status.HTTP_201_CREATED)
        except PostApplication.DoesNotExist:
            return Response({"error": "Application not found."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)