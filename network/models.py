from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass
    def __str__(self):
        return self.username

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="poster")
    post = models.CharField(max_length=64)
    date = models.DateField()

    def __str__(self):
        return f"{self.id}: a post from {self.user}. Text: {self.post} on {self.date.strftime('%d %b %Y %H:%M:%S')}"
    
class Follow(models.Model):
    profile = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True, related_name="profile")
    following = models.ManyToManyField("self", blank=True, null=True, related_name="user_followings")
    followers = models.ManyToManyField("self", blank=True, null=True, related_name="user_followers")
    
    def __str__(self):
        return str(self.profile)
    

