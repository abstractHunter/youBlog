from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models


class AuthorManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_blogger=True)


class User(AbstractUser):
    # a user is a blogger if they have verified their email address
    is_blogger = models.BooleanField(default=False)

    objects = UserManager()
    authors = AuthorManager()

    def __str__(self):
        return self.username

    @property
    def rating(self):
        """will be used to get most popular users
            most popular users are those who have the most likes and comments on their posts
            and are commenting the most on other posts
        """
        user_posts = self.posts.all()
        user_comments = self.comments.all()
        return sum([post.rating for post in user_posts]) + user_comments.count()