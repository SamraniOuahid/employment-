from django.shortcuts import render, get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework import status
from .models import Post
from .serializers import PostSerialzier, PDFDocumentSerializer
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from django.http import HttpResponse
import os
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
    # Récupérer le document PDF
    pdf_document = get_object_or_404(PDFUploadView, id=pk)
    
    # Chemin du fichier PDF
    pdf_path = pdf_document.pdf_file.path
    
    # Lire le fichier PDF cc
    with open(pdf_path, 'rb') as pdf:
        response = HttpResponse(pdf.read(), content_type='applic  ation/pdf')
        response['Content-Disposition'] = f'inline; filename="{os.path.basename(pdf_path)}"'
        return response