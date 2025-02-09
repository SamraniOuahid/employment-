from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Post, PDFDocument

class PostSerialzier(serializers.ModelSerializer):
  
    class Meta:
        model = Post
        fields= '__all__'

class PDFDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = PDFDocument
        fields = ['id', 'title', 'pdf_file', 'uploaded_at']