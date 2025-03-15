from django.contrib import admin
from django.conf import settings
from django.views.static import serve
from django.conf.urls.static import static  # Correct import
from django.urls import path, include, re_path
urlpatterns = [
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    re_path(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),  
    path('admin/', admin.site.urls),
    path('', include('blogi.urls'))
]

# Serve static and media files during development only
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)