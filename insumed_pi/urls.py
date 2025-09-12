from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include

urlpatterns = [
    # Inclui as urls do app principal
    path('', include('app.urls')),
]

if settings.DEBUG:
    # Servir arquivos de mídia durante o desenvolvimento
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
