from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from taggit.managers import TaggableManager

class Post(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=(('Draft', 'draft'), ('Published', 'published')), default='draft')
    tags = TaggableManager()

    class Meta:
        ordering = ['-timestamp']

    def get_absolute_url(self):
        return reverse("post_detail", args=[
            self.timestamp.year,
            self.timestamp.month,
            self.timestamp.day,
            self.slug
        ])
    
class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    body = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)
    is_approved = models.BooleanField(default=False)

    class Meta:
        ordering = ['-date_added']

    def __str__(self):
        return "%s - %s" % (self.post.title, self.name)



    
# Create your models here.
