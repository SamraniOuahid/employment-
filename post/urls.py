from django.urls import path
from . import views
from .views import PDFUploadView, view_pdf
urlpatterns = [
    path('new/', views.new_Post, name='new_post'),
    path('getAll/', views.get_all_post, name = 'get_all_post'),
    path('get/<str:pk>', views.get_by_id, name = 'get_by_id' ),
    path('update/<str:pk>', views.update_post, name = 'update_post' ),
    path('delete/<str:pk>', views.delete_post, name = 'delete_post' ),
    path('upload/', PDFUploadView.as_view(), name='pdf-upload'),
    path('pdf/<int:pk>/', view_pdf, name='view_pdf'),
]