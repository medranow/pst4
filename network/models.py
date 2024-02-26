from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass
    
    def __str__(self):
        return self.username

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="poster")
    post = models.CharField(max_length=64)
    date = models.DateTimeField()
    likes = models.IntegerField(default=0)
    liked = models.BooleanField(default=False)
    unliked = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.id}: a post from {self.user}. Text: {self.post} on {self.date.strftime('%d %b %Y %H:%M:%S')}"
    
    def serialize(self):
        return {
            "id": self.id,
            "user": self.user,
            "date": self.date.strftime("%b %d %Y, %I:%M %p"),
            "likes": self.likes
        }    
 
class Follow(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="userWhoIsFollowing")
    user_follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name="userWhoIsFollowed")

    def __str__(self):
        return f"{self.user} is following {self.user_follower}"

class PostFollowers(models.Model):
    user = models.ManyToManyField(User, related_name ="followedUser")
    posts = models.ManyToManyField(Post, related_name="postsOfUserFollowed")