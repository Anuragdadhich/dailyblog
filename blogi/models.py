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
        if not self.slug:  # Automatically generate slug if not provided
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def post_count(self):
        return self.post_set.count()

class Post(models.Model):
    title = models.CharField(max_length=200)
    content = HTMLField()
    image = models.ImageField(upload_to='post_images/', blank=True, null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    categories = models.ManyToManyField(Category)
    published_date = models.DateTimeField(default=timezone.now)
    views = models.PositiveIntegerField(default=0)  # To track post popularity
    slug = models.SlugField(unique=True, blank=True)  # Adding slug field
    featured = models.BooleanField(default=False)
    def save(self, *args, **kwargs):
        if not self.slug:
            # Automatically create the slug if it's not provided
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)  # Call the superclass save method

    def __str__(self):
        return self.title

    def increment_views(self):
        self.views += 1
        self.save()