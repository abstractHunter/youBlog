from django.conf import settings
from django.db import models

# Create your models here.

user_model = settings.AUTH_USER_MODEL


class Tag(models.Model):
    name = models.CharField(max_length=20)
    description = models.CharField(max_length=256, blank=True)

    def __str__(self):
        return self.name


class Post(models.Model):
    POST_STATUS = (
        (0, "Brouillon"),
        (1, "Publié"),
    )

    title = models.CharField(max_length=128)
    slug = models.CharField(max_length=128, unique=True)
    author = models.ForeignKey(user_model, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.IntegerField(choices=POST_STATUS, default=0)
    tags = models.ManyToManyField(Tag)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey(
        Post, related_name="comments", on_delete=models.CASCADE)
    author = models.ForeignKey(user_model, on_delete=models.CASCADE)
    content = models.CharField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
