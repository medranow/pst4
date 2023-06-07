from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="poster")
    post = models.CharField(max_length=64)
    date = models.DateTimeField(auto_now_add=True)
    likes = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.id}: a post from {self.user}. Text: {self.post} on {self.date.strftime('%d %b %Y %H:%M:%S')}"