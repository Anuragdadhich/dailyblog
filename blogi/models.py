from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.text import slugify
from tinymce.models import HTMLField

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def post_count(self):
        return self.post_set.count()

class Post(models.Model):
    title = models.CharField(max_length=200)
    content = HTMLField()
    image = models.ImageField(upload_to='post_images/', blank=True, null=True)  # Changed from CloudinaryField
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    categories = models.ManyToManyField(Category)
    published_date = models.DateTimeField(default=timezone.now)
    views = models.PositiveIntegerField(default=0)
    slug = models.SlugField(unique=True, blank=True)
    featured = models.BooleanField(default=False)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    def increment_views(self):
        self.views += 1
        self.save()
        
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='avatars/', default='default.jpg')
    bio = models.TextField(blank=True)
    joined_date = models.DateTimeField(auto_now_add=True)
    is_online = models.BooleanField(default=False)
    last_seen = models.DateTimeField(auto_now=True)

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    likes = models.ManyToManyField(User, related_name='liked_comments', blank=True)
    is_approved = models.BooleanField(default=True)
    is_pinned = models.BooleanField(default=False)
    
    def __str__(self):
        return f'Comment by {self.author.username} on {self.post.title}'
    
    def get_like_count(self):
        return self.likes.count()
    
    def get_reply_count(self):
        return self.children.count()

class Notification(models.Model):
    NOTIFICATION_TYPES = (
        ('comment', 'New Comment'),
        ('reply', 'New Reply'),
        ('like', 'New Like'),
        ('mention', 'Mention'),
    )
    
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, null=True, blank=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True, blank=True)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']