from rest_framework import serializers
from .models import Post, PDFDocument
from account.models import CustomUser

class PostSerializer(serializers.ModelSerializer):
    """Serializer pour le modèle Post avec les détails de l'utilisateur."""
    user = serializers.SerializerMethodField()  # Personnaliser le champ user

    class Meta:
        model = Post
        fields = '__all__'

    def get_user(self, obj):
        """Retourne les détails personnalisés de l'utilisateur, incluant company_name, company_address, company_website."""
        user = obj.user
        return {
            "id": user.id,
            "email": user.email,
            "role": user.role,
            "company_name": user.company_name,
            "company_address": user.company_address,
            "company_website": user.company_website
        }

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