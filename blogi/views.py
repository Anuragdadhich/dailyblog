from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Count, Q
from django.core.cache import cache
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
import requests
from .models import Post, Category, Comment

# =========================================================
# HOME PAGE
# =========================================================
def home(request):
    categories = Category.objects.annotate(post_count=Count('post'))
    category_posts = []
    for category in categories:
        posts = Post.objects.filter(categories=category)[:4]
        category_posts.append({
            'category': category,
            'posts': posts,
        })
    recent_posts = Post.objects.order_by('-published_date')

    paginator = Paginator(recent_posts, 8)
    page_number = request.GET.get('page')
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

# =========================================================
# POST DETAIL
# =========================================================
def post_detail(request, slug):
    categories = Category.objects.all()
    post = get_object_or_404(Post, slug=slug)
    related_posts = Post.objects.filter(categories__in=post.categories.all()).exclude(id=post.id)[:2]
    post.increment_views()
    popular_posts = Post.objects.order_by('-views')[:5]
    
    # Get top-level comments (no parent)
    comments = post.comments.filter(parent=None)
    
    context = {
        'post': post,
        'related_posts': related_posts,
        'popular_posts': popular_posts,
        'categories': categories,
        'comments': comments,
    }
    return render(request, 'post_detail.html', context)

# =========================================================
# CATEGORY POSTS
# =========================================================
def category_posts(request, slug):
    categories = Category.objects.all()
    category = get_object_or_404(Category, slug=slug)
    popular_posts = Post.objects.order_by('-views')[:5]
    posts = Post.objects.filter(categories=category)
    return render(request, 'category_post.html', {
        'category': category,
        'posts': posts,
        'popular_posts': popular_posts,
        'categories': categories
    })

# =========================================================
# POPULAR POSTS
# =========================================================
def popular_posts(request):
    categories = Category.objects.all()
    popular_posts = Post.objects.order_by('-views')[:10]
    return render(request, 'popular_posts.html', {
        'popular_posts': popular_posts,
        'categories': categories
    })

# =========================================================
# SEARCH
# =========================================================
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
        'categories': categories,
        'popular_posts': popular_posts
    })

# =========================================================
# PRIVACY
# =========================================================
def privacy(request):
    return render(request, "privacy.html")

# =========================================================
# IPL PAGE
# =========================================================
def ipl_page(request):
    api_key = "b60fb0c1eamsh236f51920ab716ep18ef8ejsnadc25e87466b"
    url = "https://cricket-live-scores.p.rapidapi.com/matches"
    headers = {
        "X-RapidAPI-Key": api_key,
        "X-RapidAPI-Host": "cricket-live-scores.p.rapidapi.com"
    }
    categories = Category.objects.all()
    popular_posts = Post.objects.order_by('-views')[:5]

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        matches = response.json().get("matches", [])
        ipl_matches = [match for match in matches if "IPL" in match.get("series", "").upper()]
        cache.set('ipl_matches', ipl_matches, 300)
        all_matches = matches
    except requests.RequestException as e:
        print(f"Error fetching data: {e}")
        ipl_matches = []
        all_matches = []

    return render(request, 'ipl_page.html', {
        'ipl_matches': ipl_matches,
        'all_matches': all_matches,
        'categories': categories,
        'popular_posts': popular_posts,
    })

# =========================================================
# COMMENTS - AJAX ENDPOINTS
# =========================================================

@login_required
def add_comment(request):
    """Add a new comment via AJAX"""
    if request.method == 'POST':
        post_id = request.POST.get('post_id')
        content = request.POST.get('content')
        parent_id = request.POST.get('parent_id')
        
        if not content or not post_id:
            return JsonResponse({'success': False, 'error': 'Missing required fields'})
        
        post = get_object_or_404(Post, id=post_id)
        
        comment = Comment.objects.create(
            post=post,
            author=request.user,
            content=content,
            parent_id=parent_id if parent_id else None
        )
        
        return JsonResponse({
            'success': True,
            'comment_id': comment.id,
            'author': comment.author.username,
            'author_id': comment.author.id,
            'content': comment.content,
            'time': comment.created_at.strftime('%b %d, %Y at %I:%M %p'),
            'likes': 0,
            'reply_count': 0,
            'is_author': True,
        })
    
    return JsonResponse({'success': False, 'error': 'Invalid request method'})

@login_required
def like_comment(request):
    """Like/unlike a comment via AJAX"""
    if request.method == 'POST':
        comment_id = request.POST.get('comment_id')
        comment = get_object_or_404(Comment, id=comment_id)
        
        if request.user in comment.likes.all():
            comment.likes.remove(request.user)
            liked = False
        else:
            comment.likes.add(request.user)
            liked = True
        
        return JsonResponse({
            'success': True,
            'liked': liked,
            'like_count': comment.likes.count()
        })
    
    return JsonResponse({'success': False, 'error': 'Invalid request method'})

@login_required
def delete_comment(request):
    """Delete a comment via AJAX"""
    if request.method == 'POST':
        comment_id = request.POST.get('comment_id')
        comment = get_object_or_404(Comment, id=comment_id)
        
        if comment.author == request.user or request.user.is_staff:
            comment.delete()
            return JsonResponse({'success': True})
        
        return JsonResponse({'success': False, 'error': 'Not authorized to delete this comment'})
    
    return JsonResponse({'success': False, 'error': 'Invalid request method'})

# =========================================================
# HTMX COMMENT (Optional - if you want to use HTMX)
# =========================================================
@login_required
def add_comment_htmx(request):
    """Add comment using HTMX (alternative to AJAX)"""
    if request.method == 'POST':
        post_id = request.POST.get('post_id')
        content = request.POST.get('content')
        post = get_object_or_404(Post, id=post_id)
        
        comment = Comment.objects.create(
            post=post,
            author=request.user,
            content=content
        )
        
        # Return HTML for the new comment
        return render(request, 'partials/comment.html', {'comment': comment})
    return HttpResponse('')