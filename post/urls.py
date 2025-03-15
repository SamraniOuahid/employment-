from django.urls import path
from . import views
from .views import PDFUploadView, CompareCVWithPost, InterviewView, SubmitInterviewResponse, EvaluateTextResponsesAPIView

urlpatterns = [
    path('new/', views.new_post, name='new_post'),
    path('getAll/', views.get_all_post, name='get_all_post'),
    path('get/<str:pk>/', views.get_by_id, name='get_by_id'),
    path('update/<str:pk>/', views.update_post, name='update_post'),
    path('delete/<str:pk>/', views.delete_post, name='delete_post'),
    path('upload/', PDFUploadView.as_view(), name='pdf-upload'),
    path('compare-cv-with-post/', CompareCVWithPost.as_view(), name='compare_cv_with_post'),
    path('interview/', InterviewView.as_view(), name='interview'),
    path('submit-interview/', SubmitInterviewResponse.as_view(), name='submit_interview'),
    path('evaluate-responses/', EvaluateTextResponsesAPIView.as_view(), name='evaluate_responses'),
]