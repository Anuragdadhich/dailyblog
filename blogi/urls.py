from django.urls import path
from .views import home,category_posts,popular_posts,post_detail,search,privacy,ipl_page  # Import your view function


urlpatterns = [
    path("", home, name="home"), 
    path('category/<slug:slug>/', category_posts, name='category_posts'),
    path('post/<slug:slug>/', post_detail, name='post_detail'),
    path('search/', search, name='search'),
    path('popular/', popular_posts, name='popular_posts'),
    path('privacy', privacy, name='privacy'),
    path('ipl/', ipl_page, name='ipl_page'),
]
