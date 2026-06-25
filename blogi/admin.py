from django.contrib import admin
from .models import Category, Post
from django.contrib import admin
from .models import Category, Post, Comment, Notification


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'post_count')

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'author', 'published_date', 'views')
    list_filter = ('categories', 'published_date')
    search_fields = ('title', 'content')
    prepopulated_fields = {'slug': ('title',)}


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['author', 'post', 'content_preview', 'created_at', 'like_count', 'is_approved']
    list_filter = ['is_approved', 'is_pinned', 'created_at']
    search_fields = ['author__username', 'content']
    actions = ['approve_comments', 'pin_comments']
    
    def content_preview(self, obj):
        return obj.content[:50] + '...' if len(obj.content) > 50 else obj.content
    content_preview.short_description = 'Content'
    
    def like_count(self, obj):
        return obj.likes.count()
    like_count.short_description = 'Likes'
    
    def approve_comments(self, request, queryset):
        queryset.update(is_approved=True)
    approve_comments.short_description = "Approve selected comments"
    
    def pin_comments(self, request, queryset):
        queryset.update(is_pinned=True)
    pin_comments.short_description = "Pin selected comments"

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ['recipient', 'sender', 'notification_type', 'is_read', 'created_at']
    list_filter = ['notification_type', 'is_read', 'created_at']
    search_fields = ['recipient__username', 'sender__username']