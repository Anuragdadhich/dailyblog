from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views  # ← Add this import

urlpatterns = [
    path("", views.home, name="home"),  # ← Use views. prefix
    path('category/<slug:slug>/', views.category_posts, name='category_posts'),
    path('post/<slug:slug>/', views.post_detail, name='post_detail'),
    path('search/', views.search, name='search'),
    path('popular/', views.popular_posts, name='popular_posts'),
    path('privacy/', views.privacy, name='privacy'),
    path('ipl/', views.ipl_page, name='ipl_page'),
    
    # Comment URLs
    path('add-comment/', views.add_comment, name='add_comment'),
    path('like-comment/', views.like_comment, name='like_comment'),
    path('delete-comment/', views.delete_comment, name='delete_comment'),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)