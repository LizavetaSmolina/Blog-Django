from django.conf import settings
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.postgres.indexes import GinIndex


class UserProfileInfo(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    bio = models.TextField(blank=True, null=False)
    date = models.DateTimeField(default=timezone.now)
    photo = models.ImageField(upload_to='profile_pics',blank=True)

    def __str__(self):
        return self.user.username

class Blog(models.Model):
    title = models.CharField(max_length=100)
    author = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    category = models.CharField(max_length=100)
    date = models.DateTimeField(default=timezone.now)
    password = models.CharField(max_length=30, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-date']

class Post(models.Model):
    blog = models.ForeignKey(Blog,on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=300)
    text = models.TextField()
    date = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    file = models.ImageField(upload_to='posts_pics',blank=True)
    password = models.CharField(max_length=30, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-date']
        indexes = [GinIndex(fields=['title'])]

class Comment(models.Model):
    post = models.ForeignKey(Post,on_delete=models.CASCADE)
    author = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    text = models.CharField(max_length=300)
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.text

    class Meta:
        ordering = ['-date']


# Create your models here.

