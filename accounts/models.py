from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    # a user is a blogger if they have verified their email address
    is_blogger = models.BooleanField(default=False)

    def __str__(self):
        return self.username
