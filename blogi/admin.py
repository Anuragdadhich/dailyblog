from django.contrib import admin
from .models import Category, Post

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'post_count')

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'author', 'published_date', 'views')
    list_filter = ('categories', 'published_date')
    search_fields = ('title', 'content')
    prepopulated_fields = {'slug': ('title',)}