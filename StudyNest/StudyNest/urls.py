from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('admin/', admin.site.urls, name='admin'),
    path('', include('courses.urls')),
    path('quizzes', include('quizzes.urls')),
    path('dashboard', include('dashboard.urls')),
    
    
     
    
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
