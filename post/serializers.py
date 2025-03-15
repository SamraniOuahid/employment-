from rest_framework import serializers
from .models import Post, PDFDocument

class PostSerializer(serializers.ModelSerializer):
    """Serializer pour le modèle Post."""
    class Meta:
        model = Post
        fields = '__all__'

class PDFDocumentSerializer(serializers.ModelSerializer):
    """Serializer pour le modèle PDFDocument (CVs)."""
    class Meta:
        model = PDFDocument
        fields = ['id', 'title', 'pdf_file', 'uploaded_at']

    def validate_pdf_file(self, value):
        """Valide que le fichier uploadé est un PDF."""
        if not value.name.endswith('.pdf'):
            raise serializers.ValidationError("Seuls les fichiers PDF sont autorisés.")
        return value

class EvaluateResponsesSerializer(serializers.Serializer):
    """Serializer pour évaluer les réponses textuelles des candidats."""
    post_id = serializers.IntegerField(required=True)
    candidate_answers = serializers.ListField(
        child=serializers.CharField(),
        required=True
    )