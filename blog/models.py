from django.conf import settings
from django.db import models
from django.template.defaultfilters import slugify
from datetime import datetime

from taggit.managers import TaggableManager

# Create your models here.

user_model = settings.AUTH_USER_MODEL


class PublishedPostsManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(published=True)


class Post(models.Model):
    title = models.CharField(max_length=128)
    thumbnail = models.ImageField(
        upload_to='uploads/blog/thumbnails/%Y/%m/%d/', blank=True)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    author = models.ForeignKey(user_model, on_delete=models.CASCADE, related_name='posts')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published = models.BooleanField(default=False)
    likes = models.ManyToManyField(
        to=user_model, related_name='likes', blank=True)
    tags = TaggableManager(blank=True)

    objects = models.Manager()
    published_objects = PublishedPostsManager()

    @property
    def rating(self):
        # will be used to get most popular posts
        return self.likes.count() + self.comments.count()

    class Meta:
        ordering = ["-created_at"]

    def _generate_unique_slug(self):
        slug = slugify(self.title)
        unique_slug = "{}-{}".format(slug,
                                     datetime.now().strftime("%Y-%b-%d-%H-%M-%S"))  # like 2020-Jul-01-12-50-22
        return unique_slug

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self._generate_unique_slug()
        super(Post, self).save(*args, **kwargs)

    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey(
        Post, related_name="comments", on_delete=models.CASCADE)
    author = models.ForeignKey(user_model, on_delete=models.CASCADE, related_name='comments')
    content = models.CharField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
