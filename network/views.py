from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.http import JsonResponse
from datetime import datetime

from .models import User, Post, Follow


def index(request):
    if request.user.is_authenticated:
        posts = Post.objects.all()
        return render(request, "network/index.html", {
            "posts": posts,
        })
    else:
        posts = Post.objects.all()
        return render(request, "network/index.html", {
            "posts": posts,
        })



def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")
    
# Allows to post a new post and save it in the database
def new_post(request):
   if request.method == "POST":
       user = request.user
       text = request.POST["text-compose"]
       post = Post(
           user = user,
           post = text,
           date = datetime.now()
       )
       post.save()
       #JsonResponse("success")
       return HttpResponseRedirect(reverse("index"))
   else:
       render(request, "network/index.html")

# Renders a profile page
def profile(request, user_id):
    if request.user.is_authenticated:
        posts = Post.objects.filter(user=user_id).order_by('-date')
        follows = Follow.objects.all()
        return render(request, "network/profile.html", {
            'posts': posts,
            'follows': follows
        })
    else:
        posts = Post.objects.filter(user=user_id).order_by('-date')
        return render(request, "network/profile.html", {
            'posts': posts,
        })

# Increase followers and followings
def followerCount(request, userFollow):
    if request.user.is_authenticated:
        if request.method == "POST":
                    

                    #Declare variables for sum
                    countPlusFollow = 0
                    if countPlusFollow <= countPlusFollow:
                        countPlusFollow += 1

                    # Create user following
                    new_following = Follow (
                        numberFollowings = countPlusFollow,
                        # I use _id because I need an integer as a reference
                        following_id = userFollow,
                        profile = request.user
                    )
                    new_following.save()
            
                    #Update user being followed
                    new_follower = Follow (
                        numberFollowers = countPlusFollow,
                        followers = request.user,
                        # I use profile_id because I need an integer reference
                        profile_id = userFollow
                    )
                    new_follower.save()

                    

        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/test.html")

# Decrease the count of follower and following
def followDecrease(request, user_id):
    pass