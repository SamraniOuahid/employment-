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
        def validate_pdf_file(self, value):
        # Vérifier si le fichier est un PDF
            if not value.name.endswith('.pdf'):
                raise serializers.ValidationError("Seuls les fichiers PDF sont autorisés.")
            return value