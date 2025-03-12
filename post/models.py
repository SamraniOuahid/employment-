from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
import os
from django.utils.timezone import now
# Model representing a job post
class Post(models.Model):
    """Represents a job post."""
    title = models.CharField(max_length=200, blank=False, help_text="Title of the job post")
    description = models.TextField(blank=False, help_text="Detailed description of the job post")
    final_date = models.DateField(blank=True, null=True, help_text="Application deadline for the job post")
    uploaded_at = models.DateTimeField(default=now, help_text="Date and time when the post was created")
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, help_text="User who created the job post")
    accepted = models.BooleanField(default=False, help_text="Indicates if the candidate has been accepted")

    def __str__(self):
        return self.title


# Model representing an uploaded PDF document (e.g., a CV)
class PDFDocument(models.Model):
    """Represents an uploaded PDF document (e.g., a resume)."""
    title = models.CharField(max_length=255, help_text="Title of the PDF document")
    pdf_file = models.FileField(
        upload_to='pdfs/',
        help_text="Uploaded PDF file",
    )
    uploaded_at = models.DateTimeField(auto_now_add=True, help_text="Date and time when the file was uploaded")

    def __str__(self):
        return self.title

    def clean(self):
        """Validates that only PDF files are uploaded."""
        super().clean()
        if not self.pdf_file.name.endswith('.pdf'):
            raise ValidationError("Only PDF files are allowed.")

    def save(self, *args, **kwargs):
        """Validates before saving."""
        self.clean()
        super().save(*args, **kwargs)


# Model representing a response in an interview
class InterviewResponse(models.Model):
    """Represents a candidate's response during an interview."""
    user = models.ForeignKey(User, on_delete=models.CASCADE, help_text="User who provided the response")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, help_text="Job post associated with the interview")
    question = models.TextField(help_text="Interview question asked to the candidate")
    answer = models.TextField(help_text="Candidate's response to the question")
    timestamp = models.DateTimeField(auto_now_add=True, help_text="Timestamp when the response was recorded")
    approved = models.BooleanField(default=False, help_text="Indicates if the response is approved")
    score = models.FloatField(default=0.0, help_text="Score assigned to the response")

    def __str__(self):
        return f"Response from {self.user.username} for {self.post.title}"

    def calculate_score(self, ideal_answer):
        """
        Calculates the similarity score between the candidate's answer and the ideal answer.
        
        Args:
            ideal_answer (str): The ideal or expected answer for the question.
        """
        from sklearn.feature_extraction.text import TfidfVectorizer
        from sklearn.metrics.pairwise import cosine_similarity

        vectorizer = TfidfVectorizer().fit_transform([self.answer, ideal_answer])
        vectors = vectorizer.toarray()
        similarity_score = cosine_similarity([vectors[0]], [vectors[1]])[0][0]
        self.score = round(similarity_score * 100, 2)
        self.save()


# Model representing a report generated after an interview
class Report(models.Model):
    """Represents a report generated after an interview."""
    user = models.ForeignKey(User, on_delete=models.CASCADE, help_text="User associated with the report")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, help_text="Job post associated with the report")
    date = models.DateField(auto_now_add=True, help_text="Date when the report was generated")
    message = models.TextField(blank=False, help_text="Content of the report")

    def __str__(self):
        return f"Report for {self.post.title} - {self.user.username}"

    @staticmethod
    def generate_report(user, post):
        """
        Generates a report based on the candidate's responses.

        Args:
            user (User): The user (candidate) for whom the report is being generated.
            post (Post): The job post associated with the interview.

        Returns:
            Report: The generated report object.
        """
        responses = InterviewResponse.objects.filter(user=user, post=post)
        total_score = sum(response.score for response in responses)
        average_score = round(total_score / len(responses), 2) if responses else 0.0

        message = (
            f"Report for candidate {user.username} on the job post '{post.title}'.\n"
            f"Final score: {average_score}%.\n"
            "Details of scores:\n"
        )
        for i, response in enumerate(responses, start=1):
            message += f"Response {i}: {response.score}%\n"

        report, created = Report.objects.get_or_create(user=user, post=post)
        report.message = message
        report.save()
        return report


# Model representing a notification
class Notification(models.Model):
    """Represents a notification sent to a user."""
    user = models.ForeignKey(User, on_delete=models.CASCADE, help_text="User receiving the notification")
    notification = models.TextField(help_text="Message of the notification")
    read = models.BooleanField(default=False, help_text="Indicates if the notification has been read")
    created_at = models.DateTimeField(auto_now_add=True, help_text="Date and time when the notification was created")

    def __str__(self):
        return f"Notification for {self.user.username}"