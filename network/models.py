from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="poster")
    post = models.CharField(max_length=64)
    date = models.DateField()

    def __str__(self):
        return f"{self.id}: a post from {self.user}. Text: {self.post} on {self.date.strftime('%d %b %Y %H:%M:%S')}"
    
class Follower(models.Model):
    user = models.ForeignKey(User,blank=True, null=True, on_delete=models.CASCADE, 
    related_name="num_followers")
    numberFollowers = models.IntegerField(default=0)
    following = models.ManyToManyField(User, blank=True, null=True, related_name="user_following")
