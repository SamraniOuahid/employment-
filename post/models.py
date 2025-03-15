from django.db import models
from django.conf import settings
from django.utils.timezone import now
from django.core.exceptions import ValidationError

class Post(models.Model):
    """Modèle représentant un poste d'emploi."""
    title = models.CharField(max_length=200, blank=False, help_text="Titre du poste")
    description = models.TextField(blank=False, help_text="Description détaillée du poste")
    final_date = models.DateField(blank=True, null=True, help_text="Date limite de candidature")
    uploaded_at = models.DateTimeField(default=now, help_text="Date et heure de création")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, help_text="Utilisateur ayant créé le poste")
    accepted = models.BooleanField(default=False, help_text="Indique si un candidat a été accepté")

    def __str__(self):
        return self.title

class PDFDocument(models.Model):
    """Modèle représentant un document PDF uploadé (par exemple, un CV)."""
    title = models.CharField(max_length=255, help_text="Titre du document PDF")
    pdf_file = models.FileField(upload_to='pdfs/', help_text="Fichier PDF uploadé")
    uploaded_at = models.DateTimeField(auto_now_add=True, help_text="Date et heure d'upload")

    def __str__(self):
        return self.title

    def clean(self):
        """Valide que seuls les fichiers PDF sont uploadés."""
        if not self.pdf_file.name.endswith('.pdf'):
            raise ValidationError("Seuls les fichiers PDF sont autorisés.")

    def save(self, *args, **kwargs):
        """Valide avant de sauvegarder."""
        self.clean()
        super().save(*args, **kwargs)

class InterviewResponse(models.Model):
    """Modèle représentant une réponse d'un candidat lors d'un entretien."""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, help_text="Utilisateur ayant fourni la réponse")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, help_text="Poste associé à l'entretien")
    question = models.TextField(help_text="Question posée au candidat")
    answer = models.TextField(help_text="Réponse du candidat")
    timestamp = models.DateTimeField(auto_now_add=True, help_text="Horodatage de la réponse")
    approved = models.BooleanField(default=False, help_text="Indique si la réponse est approuvée")
    score = models.FloatField(default=0.0, help_text="Score attribué à la réponse")

    def __str__(self):
        return f"Response from {self.user.username} for {self.post.title}"

class Notification(models.Model):
    """Modèle représentant une notification envoyée à un utilisateur."""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, help_text="Utilisateur recevant la notification")
    notification = models.TextField(help_text="Message de la notification")
    read = models.BooleanField(default=False, help_text="Indique si la notification a été lue")
    created_at = models.DateTimeField(auto_now_add=True, help_text="Date et heure de création")

    def __str__(self):
        return f"Notification for {self.user.username}"