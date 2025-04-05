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
    if post.user != request.user:
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

        if similarity_score > 0.5:
            return Response({
                "message": "You are eligible for an interview.",
                "similarity_score": round(similarity_score * 100, 2),
                "next_step": "interview"
            })
        return Response({
            "message": "Sorry, you are not eligible for an interview.",
            "similarity_score": round(similarity_score * 100, 2)
        })

# Generate interview questions
class InterviewView(APIView):
    def post(self, request, *args, **kwargs):
        post_id = request.data.get('post_id')
        try:
            post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            return Response({"error": "Post not found."}, status=status.HTTP_404_NOT_FOUND)

        questions = generate_questions(post.description, num_questions=5)
        return Response({
            "questions": questions,
            "post_title": post.title
        })

# Submit text responses for interview
class SubmitInterviewResponse(APIView):
    def post(self, request, *args, **kwargs):
        post_id = request.data.get('post_id')
        responses = request.data.get('responses')  # Expected format: [{"question": "...", "answer": "..."}, ...]

        try:
            post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            return Response({"error": "Post not found."}, status=status.HTTP_404_NOT_FOUND)

        if not responses or not isinstance(responses, list):
            return Response({"error": "Responses must be a list."}, status=status.HTTP_400_BAD_REQUEST)

        for response in responses:
            question = response.get('question')
            answer = response.get('answer')
            if not question or not answer:
                return Response({"error": "Each response must have a question and an answer."}, status=status.HTTP_400_BAD_REQUEST)
            InterviewResponse.objects.create(
                user=request.user,
                post=post,
                question=question,
                answer=answer
            )

        return Response({"message": "Text responses submitted successfully."}, status=status.HTTP_200_OK)

# Evaluate text responses
class EvaluateTextResponsesAPIView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = EvaluateResponsesSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        post_id = serializer.validated_data['post_id']
        candidate_answers = serializer.validated_data['candidate_answers']

        try:
            post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            return Response({"error": "Post not found."}, status=status.HTTP_404_NOT_FOUND)

        final_score, scores = evaluate_responses(candidate_answers, post.description)

        # Save scores to InterviewResponse (optional)
        responses = InterviewResponse.objects.filter(user=request.user, post=post).order_by('timestamp')[:len(candidate_answers)]
        for response, score in zip(responses, scores):
            response.score = score
            response.save()

        # Create notification if score is sufficient
        # if final_score > 70:
        #     Notification.objects.create(
        #         user=request.user,
        #         notification=f"Congratulations! You passed the virtual interview for {post.title}. Please attend an in-person interview."
        #     )

        return Response({
            "final_score": final_score,
            "scores": scores,
            "post_title": post.title,
            "message": "Text response evaluation completed."
        }, status=status.HTTP_200_OK)
    







@api_view(['POST'])
@permission_classes([IsAuthenticated])
def apply_to_post(request):
    post_id = request.data.get('post_id')
    try:
        post = Post.objects.get(id=post_id)
        # Vérifier si l'utilisateur a déjà postulé
        if PostApplication.objects.filter(post=post, user=request.user).exists():
            return Response({"error": "Vous avez déjà postulé à ce poste"}, status=status.HTTP_400_BAD_REQUEST)
        
        # Créer une candidature
        application = PostApplication.objects.create(
            post=post,
            user=request.user
        )
        return Response({
            "application": {
                "post_id": post.id,
                "user_id": request.user.id,
                "status": application.status,
                "application_date": application.application_date
            }
        }, status=status.HTTP_201_CREATED)
    except Post.DoesNotExist:
        return Response({"error": "Poste non trouvé"}, status=status.HTTP_404_NOT_FOUND)
    




@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def update_application_status(request):
    application_id = request.data.get('application_id')
    new_status = request.data.get('status')

    try:
        application = PostApplication.objects.get(id=application_id, post__user=request.user)
        if new_status not in ['accepte', 'refuse', 'en_attente']:
            return Response({"error": "Statut invalide"}, status=status.HTTP_400_BAD_REQUEST)
        
        application.status = new_status
        application.save()
        return Response({
            "application": {
                "id": application.id,
                "post_id": application.post.id,
                "user_id": application.user.id,
                "status": application.status
            }
        }, status=status.HTTP_200_OK)
    except PostApplication.DoesNotExist:
        return Response({"error": "Candidature non trouvée ou non autorisée"}, status=status.HTTP_404_NOT_FOUND)