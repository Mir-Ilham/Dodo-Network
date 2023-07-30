from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    name = models.CharField(max_length=200, null=True)
    email = models.EmailField(unique=True, null=True)
    bio = models.TextField(null=True)
    company_name = models.CharField(max_length=200, null=True)
    profile_picture = models.ImageField(null=True, default="avatar.svg")

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

class BlogPost(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    cover = models.ImageField(null=True, default='cover.svg')
    title = models.CharField(max_length=500, null=True)
    content = models.TextField(null=True)

    def __str__(self):
        return self.title[0:50]

class Topic(models.Model):
    name = models.CharField(max_length=200)
    experts = models.ManyToManyField(User, related_name="experts", blank=True)

    def __str__(self):
        return self.name

class Room(models.Model):
    host = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    participants = models.ManyToManyField(User, related_name='participants', blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-updated', '-created']

    def __str__(self):
        return self.name

class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    body = models.TextField()
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-updated', '-created']

    def __str__(self):
        return self.body[0:50]