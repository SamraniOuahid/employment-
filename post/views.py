from django.shortcuts import render, get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework import status
from .models import Post, PDFDocument, InterviewResponse
from .serializers import PostSerialzier, PDFDocumentSerializer
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from django.http import HttpResponse
import os
from .ai_algorithm import compare_cv_with_post
from .utils import extract_text_from_pdf
from .ai_question_generator import generate_questions
from django.conf import settings
from .speech_to_text import transcribe_audio
# Create your views here.
# get All
@api_view(['GET'])
def get_all_post(request):
    post = Post.objects.all()
    serializer = PostSerialzier(post, many=True)
    print(post)
    return Response({"post":serializer.data})

#get post by id
@api_view(['GET'])
def get_by_id(request, pk):
    post = get_object_or_404(Post, id=pk)
    serializer = PostSerialzier(post, many=False)
    print(post)
    return Response({"posts":serializer.data})

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def new_Post(request):
    data = request.data
    serializer = PostSerialzier(data = data)
    if serializer.is_valid():
        post = Post.objects.create(**data, user = request.user)
        res = PostSerialzier(post, many=False)
        return Response({"post":res.data})
    else:
        return Response(serializer.errors)
    
# update

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_post(request,pk):
    post = get_object_or_404(Post,id=pk)

    if post.user != request.user:
        return Response({"error":"Sorry you can not update this post"}
                        , status=status.HTTP_403_FORBIDDEN)
    
    post.title = request.data['title']
    post.description = request.data['description']
    post.dateFin = request.data['dateFin']
    post.save()
    serializer = PostSerialzier(post,many=False)
    return Response({"post":serializer.data})


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_post(request,pk):
    post = get_object_or_404(Post,id=pk)

    if post.user != request.user:
        return Response({"error":"Sorry you can not update this post"}
                        , status=status.HTTP_403_FORBIDDEN)
    
    
    post.delete()
    
    return Response({"post":"The post is deleted"}, status=status.HTTP_200_OK)



class PDFUploadView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        serializer = PDFDocumentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
    
def view_pdf(request, pk):
    # Récupérer le document PDF depuis le modèle PDFDocument
    pdf_document = get_object_or_404(PDFDocument, id=pk)
    
    # Chemin du fichier PDF
    pdf_path = pdf_document.pdf_file.path
    
    # Vérifier si le fichier existe
    if not os.path.exists(pdf_path):
        return HttpResponse("Fichier PDF introuvable", status=404)
    
    # Lire le fichier PDF
    with open(pdf_path, 'rb') as pdf:
        response = HttpResponse(pdf.read(), content_type='application/pdf')
        response['Content-Disposition'] = f'inline; filename="{os.path.basename(pdf_path)}"'
        return response
    

class CompareCVWithPost(APIView):
    def post(self, request, *args, **kwargs):
        cv_id = request.data.get('cv_id')
        post_id = request.data.get('post_id')

        try:
            pdf_document = PDFDocument.objects.get(id=cv_id)
            post = Post.objects.get(id=post_id)
        except (PDFDocument.DoesNotExist, Post.DoesNotExist):
            return Response({"error": "CV ou poste introuvable."}, status=404)

        cv_text = extract_text_from_pdf(pdf_document.pdf_file.path)
        similarity_score = compare_cv_with_post(cv_text, post.description)

        if similarity_score > 0.5:  # Seuil de 50%
            return Response({
                "message": "Vous êtes éligible pour un entretien.",
                "similarity_score": round(similarity_score * 100, 2),
                "next_step": "interview"
            })
        else:
            return Response({
                "message": "Désolé, vous n'êtes pas éligible pour un entretien.",
                "similarity_score": round(similarity_score * 100, 2)
            })
        


class InterviewView(APIView):
    def post(self, request, *args, **kwargs):
        post_id = request.data.get('post_id')

        try:
            post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            return Response({"error": "Poste introuvable."}, status=404)

        # Générer des questions
        questions = generate_questions(post.description, num_questions=5)

        return Response({
            "questions": questions,
            "post_title": post.title
        })
    

class SubmitInterviewResponse(APIView):
    def post(self, request, *args, **kwargs):
        post_id = request.data.get('post_id')
        responses = request.data.get('responses')  # Liste de {question: ..., answer: ...}

        try:
            post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            return Response({"error": "Poste introuvable."}, status=404)

        for response in responses:
            question = response.get('question')
            answer = response.get('answer')
            InterviewResponse.objects.create(
                user=request.user,
                post=post,
                question=question,
                answer=answer
            )

        return Response({"message": "Réponses soumises avec succès."})
    




class SubmitVoiceResponse(APIView):
    def post(self, request, *args, **kwargs):
        post_id = request.data.get('post_id')
        audio_file = request.FILES.get('audio_file')  # Fichier audio soumis par l'utilisateur
        question = request.data.get('question')

        try:
            post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            return Response({"error": "Poste introuvable."}, status=404)

        if not audio_file:
            return Response({"error": "Aucun fichier audio fourni."}, status=400)

        # Sauvegarder temporairement le fichier audio
        temp_audio_path = os.path.join(settings.MEDIA_ROOT, audio_file.name)
        with open(temp_audio_path, 'wb+') as destination:
            for chunk in audio_file.chunks():
                destination.write(chunk)

        # Transcrire le fichier audio
        try:
            transcribed_text = transcribe_audio(temp_audio_path)
        except Exception as e:
            os.remove(temp_audio_path)  # Nettoyer le fichier temporaire en cas d'erreur
            return Response({"error": f"Erreur lors de la transcription : {str(e)}"}, status=500)

        # Enregistrer la réponse dans la base de données
        InterviewResponse.objects.create(
            user=request.user,
            post=post,
            question=question,
            answer=transcribed_text
        )

        # Supprimer le fichier temporaire après traitement
        os.remove(temp_audio_path)

        return Response({"message": "Réponse vocale transmise avec succès.", "transcribed_text": transcribed_text})