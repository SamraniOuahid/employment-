from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('admin/', admin.site.urls),
    # path('api/', include('myapp.urls')),  
    path('api/', include('account.urls')),  
    path('api/token/', TokenObtainPairView.as_view()),  
    path('post/', include('post.urls'))
      # Inclure les routes de l'API
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)