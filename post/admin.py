from django.contrib import admin
from .models import Post, PDFDocument, InterviewResponse

admin.site.register(Post)
admin.site.register(PDFDocument)
admin.site.register(InterviewResponse)