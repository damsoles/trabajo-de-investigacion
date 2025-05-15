from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from core.views import home

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('core/', include('core.urls', namespace='core')),  
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
