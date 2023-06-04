from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="poster")
    post = models.TextField(blank=True)

    def __str__(self):
        return f"{self.id}: a post from {self.user}. Test: {self.post}"