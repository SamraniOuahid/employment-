from django.db import models
from django.conf import settings
from django.utils.timezone import now, timedelta
from django.core.exceptions import ValidationError

class Post(models.Model):
    """Modèle représentant un poste d'emploi."""
    title = models.CharField(max_length=200, blank=False, help_text="Titre du poste")
    description = models.TextField(blank=False, help_text="Description détaillée du poste")
    final_date = models.DateField(blank=True, null=True, help_text="Date limite de candidature")
    salaire = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, help_text="Salaire proposé en DH")
    uploaded_at = models.DateTimeField(default=now, help_text="Date et heure de création")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, help_text="Utilisateur ayant créé le poste")
    

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
    # approved = models.BooleanField(default=False, help_text="Indique si la réponse est approuvée")
    score = models.FloatField(default=0.0, help_text="Score attribué à la réponse")

    def __str__(self):
        return f"Response from {self.user.username} for {self.post.title}"




class PostApplication(models.Model):
    STATUS_CHOICES = (
        ('en_attente', 'En attente'),
        ('accepte', 'Accepté'),
        ('refuse', 'Refusé'),
    )
    INTERVIEW_STEPS = (
        ('pending', 'En attente'),
        ('cv_compared', 'CV comparé'),
        ('interview_saved', 'Interview sauvegardé'),
        ('questions_generated', 'Questions générées'),
        ('answers_submitted', 'Réponses soumises'),
        ('evaluated', 'Évalué'),
    )

    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    application_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='en_attente')
    cv = models.ForeignKey(PDFDocument, on_delete=models.SET_NULL, null=True, blank=True)
    interview = models.ForeignKey('Interview', on_delete=models.SET_NULL, null=True, blank=True)
    step = models.CharField(max_length=20, choices=INTERVIEW_STEPS, default='pending')  # Nouveau champ pour suivre l'étape

    def __str__(self):
        return f"{self.user.email} - {self.post.title} ({self.status})"
    

    
class Report(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, help_text="Poste signalé")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, help_text="Utilisateur qui signale")
    description = models.TextField(help_text="Raison du signalement (ex. : salaire incorrect)")
    reported_at = models.DateTimeField(auto_now_add=True, help_text="Date du signalement")

    def __str__(self):
        return f"Signalement de {self.user.email} pour {self.post.title}"






class Interview(models.Model):
    STATUS_CHOICES = (
        ('planned', 'Planifié'),
        ('in_progress', 'En cours'),
        ('completed', 'Terminé'),
    )

    post = models.ForeignKey('Post', on_delete=models.CASCADE, help_text="Poste lié à l’entretien")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, help_text="Candidat passant l’entretien")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='planned', help_text="Statut de l’entretien")
    start_date = models.DateTimeField(default=now, help_text="Date de début (automatique à la création)")
    end_date = models.DateTimeField(help_text="Date de fin (24h après le début)")
    questions = models.JSONField(null=True, blank=True, help_text="Questions posées (format JSON)")
    responses = models.JSONField(null=True, blank=True, help_text="Réponses du candidat (format JSON)")
    score = models.FloatField(null=True, blank=True, help_text="Score attribué à l’entretien")

    def save(self, *args, **kwargs):
        if not self.id:  # Si nouvelle instance
            self.end_date = self.start_date + timedelta(hours=24)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Entretien pour {self.post.title} - {self.user.email} ({self.status})"