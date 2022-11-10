from django.db import models
from django.conf import settings



# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=50)
    day = models.DateTimeField()
    time = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    like_user = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="like_post")
    park_address = models.CharField(max_length=80)
    pet = models.BooleanField(default = False)
    content = models.TextField()

class Comment(models.Model):
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)