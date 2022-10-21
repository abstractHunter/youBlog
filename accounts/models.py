from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    # a user is a blogger if they have verified their email address
    is_blogger = models.BooleanField(default=False)
    pass

    def __str__(self):
        return self.username
