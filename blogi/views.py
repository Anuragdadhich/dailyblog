from django.shortcuts import render
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Post, Category  
from django.db.models import Count
import requests
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.cache import cache
def home(request):
    categories = Category.objects.annotate(post_count=Count('post'))
    category_posts = []
    for category in categories:
        posts = Post.objects.filter(categories=category)[:4] #4post
        category_posts.append({
            'category': category,
            'posts': posts,
        })
    recent_posts = Post.objects.order_by('-published_date')

    paginator = Paginator(recent_posts, 6)  #perpage post
    page_number = request.GET.get('page')  #current url
    try:
        page_obj = paginator.page(page_number) 
    except PageNotAnInteger:
        page_obj = paginator.page(1) 
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages) 
        
    popular_posts = Post.objects.order_by('-views')[:4]

    featured_posts = Post.objects.filter(featured=True)[:3]

    context = {
        'categories': categories, 
        'category_posts': category_posts,  
        'recent_posts': page_obj, 
        'popular_posts': popular_posts,
        'featured_posts': featured_posts,
        'page_obj': page_obj,  
    }
    return render(request, 'home.html', context)
def category_posts(request, slug):
    categories = Category.objects.all() 
    category = get_object_or_404(Category, slug=slug)
    popular_posts = Post.objects.order_by('-views')[:5]
    posts = Post.objects.filter(categories=category)
    return render(request, 'category_post.html', {'category': category, 'posts': posts,popular_posts:'popular_posts','categories':categories})

def popular_posts(request):
    categories = Category.objects.all() 
    popular_posts = Post.objects.order_by('-views')[:10]  # Fetching 10 popular posts
    return render(request, 'popular_posts.html', {
        'popular_posts': popular_posts,
        'categories':categories
    })

def post_detail(request, slug):
    categories = Category.objects.all() 
    post = get_object_or_404(Post, slug=slug)
    related_posts = Post.objects.filter(categories__in=post.categories.all()).exclude(id=post.id)[:2]  #
    post.increment_views()
    popular_posts = Post.objects.order_by('-views')[:5]
    return render(request, 'post_detail.html', {'post': post, 'related_posts': related_posts,'popular_posts': popular_posts,'categories':categories})

def search(request):
    popular_posts = Post.objects.order_by('-views')[:5]
    categories = Category.objects.all() 
    query = request.GET.get('q')  
    if query:
        posts = Post.objects.filter(
            Q(title__icontains=query) | Q(content__icontains=query)
        ).distinct()  
    else:
        posts = Post.objects.none()  

    return render(request, 'search.html', {
        'posts': posts,
        'query': query,
        'categories':categories,
        'popular_posts':popular_posts
    })
def privacy(request):
    return render(request, "privacy.html")
#1058580b-1dda-4fc3-affe-6e2768e04a38
#ef4e8a14dbmshcc83adecddfed7dp1523dfjsnd3bda996966e
def ipl_page(request):
    api_key = "b60fb0c1eamsh236f51920ab716ep18ef8ejsnadc25e87466b"  # Replace with your RapidAPI key
    url = "https://cricket-live-scores.p.rapidapi.com/matches"
    headers = {
        "X-RapidAPI-Key": api_key,
        "X-RapidAPI-Host": "cricket-live-scores.p.rapidapi.com"
    }
    categories = Category.objects.all()
    popular_posts = Post.objects.order_by('-views')[:5]

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an exception for HTTP errors
        matches = response.json().get("matches", [])

        # Filter IPL matches (flexible condition)
        ipl_matches = [match for match in matches if "IPL" in match.get("series", "").upper()]

        # Cache the data for 5 minutes (300 seconds)
        cache.set('ipl_matches', ipl_matches, 300)
        all_matches = matches
    except requests.RequestException as e:
        print(f"Error fetching data: {e}")
        print(f"API Response: {response.text if 'response' in locals() else 'No response'}")
        ipl_matches = []
        all_matches = []

    return render(request, 'ipl_page.html', {
        'ipl_matches': ipl_matches,
        'all_matches': all_matches,
        'categories': categories,
        'popular_posts': popular_posts,
    })
