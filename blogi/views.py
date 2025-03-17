from django.shortcuts import render
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Post, Category  # Import models
from django.db.models import Count
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def home(request):
    # Fetch all categories with their posts (limit to 4 posts per category)
    categories = Category.objects.annotate(post_count=Count('post'))
    category_posts = []
    for category in categories:
        posts = Post.objects.filter(categories=category)[:4]  # Limit to 4 posts per category
        category_posts.append({
            'category': category,
            'posts': posts,
        })

    # Fetch recent posts (full queryset for pagination)
    recent_posts = Post.objects.order_by('-published_date')

    # Paginate recent posts
    paginator = Paginator(recent_posts, 6)  # Show 4 posts per page
    page_number = request.GET.get('page')  # Get the current page number from the URL
    try:
        page_obj = paginator.page(page_number)  # Get the current page
    except PageNotAnInteger:
        page_obj = paginator.page(1)  # Default to the first page
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)  # Deliver the last page if page is out of range

    # Fetch popular posts (optional)
    popular_posts = Post.objects.order_by('-views')[:7]

    # Fetch featured posts (optional)
    featured_posts = Post.objects.filter(featured=True)[:3]

    context = {
        'categories': categories, 
        'category_posts': category_posts,  # List of categories with their posts
        'recent_posts': page_obj,  # Use paginated recent posts
        'popular_posts': popular_posts,
        'featured_posts': featured_posts,
        'page_obj': page_obj,  # Pass the paginator object to the template
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
    popular_posts = Post.objects.order_by('-views')[:10]  # Fetch top 10 popular posts
    return render(request, 'popular_posts.html', {
        'popular_posts': popular_posts,
        'categories':categories
    })

def post_detail(request, slug):
    categories = Category.objects.all() 
    post = get_object_or_404(Post, slug=slug)
    related_posts = Post.objects.filter(categories__in=post.categories.all()).exclude(id=post.id)[:2]  # Fetch related posts
    post.increment_views()  # Increment view count
    popular_posts = Post.objects.order_by('-views')[:5]
    return render(request, 'post_detail.html', {'post': post, 'related_posts': related_posts,'popular_posts': popular_posts,'categories':categories})

def search(request):
    popular_posts = Post.objects.order_by('-views')[:5]
    categories = Category.objects.all() 
    query = request.GET.get('q')  # Get the search query from the URL
    if query:
        # Filter posts by title or content
        posts = Post.objects.filter(
            Q(title__icontains=query) | Q(content__icontains=query)
        ).distinct()  # Ensure no duplicate results
    else:
        posts = Post.objects.none()  # Return no results if no query is provided

    return render(request, 'search.html', {
        'posts': posts,
        'query': query,
        'categories':categories,
        'popular_posts':popular_posts
    })
def privacy(request):
    return render(request, "privacy.html")