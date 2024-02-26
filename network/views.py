from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.http import JsonResponse
from datetime import datetime
from django.core.paginator import Paginator
from django.views.generic import ListView
from django.http import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt

from .models import User, Post, Follow

# Added a class of ListView to view my post model items
class PostsListView(ListView):
    paginate_by = 2
    model = Post


def index(request):
    if request.user.is_authenticated:
        # Obtain all posts
        posts = Post.objects.all().order_by("-date")

        #Paginate
        paginator = Paginator(posts, 2) #show 2 posts per page
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        return render(request, "network/index.html", {
            "page_obj": page_obj,
        })
    else:
        return render(request, "network/index.html")



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
        user = User.objects.get(pk=user_id)
        posts = Post.objects.filter(user=user_id).order_by('-date')

        # Get the number of follows
        following = Follow.objects.filter(user=user)
        followers = Follow.objects.filter(user_follower=user)

        try:
            checkFollow = followers.filter(user=User.objects.get(pk=request.user.id))
            if len(checkFollow) != 0:
                isFollowing = True
            else:
                isFollowing = False
        except:
            isFollowing =False

        # Pagination for profiles
        paginator = Paginator(posts, 2) #show 2 posts per page
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        
        return render(request, "network/profile.html", {
            'page_obj': page_obj,
            'userName': user.username,
            'following': following,
            'followers': followers,
            'isFollowing': isFollowing,
            'user_profile': user,
            
        })
    else:
        posts = Post.objects.filter(user=user_id).order_by('-date')
        return render(request, "network/profile.html", {
            'posts': posts,
        })

# Follow
def follow(request):
    userFollower = request.POST['userfollow']
    currentUser = User.objects.get(pk=request.user.id)
    userFollowData = User.objects.get(username=userFollower)
    f = Follow(
        user = currentUser,
        user_follower = userFollowData
    )
    f.save()

    user_id = userFollowData.id 
    
    return HttpResponseRedirect(reverse(profile, kwargs={'user_id': user_id}))


# Unfollow
def unfollow(request):
    userFollower = request.POST["userfollow"]
    currentUser = User.objects.get(pk=request.user.id)
    userFollowData = User.objects.get(username=userFollower)
    f = Follow.objects.get(
        user = currentUser,
        user_follower = userFollowData
    )
    f.delete()

    user_id = userFollowData.id 
    
    return HttpResponseRedirect(reverse(profile, kwargs={'user_id': user_id}))

def following(request):
    if request.user.is_authenticated:
        followUsers = Follow.objects.filter(user=request.user.id)
        posts = Post.objects.all().order_by('-date')

        # Obtain all posts of people followed
        postPrint = []
        for user in followUsers:
            for post in posts:
                if user.user_follower == post.user:
                    postPrint.append(post)
                    

        # Pagination
        paginator = Paginator(postPrint, 2) #show 2 posts per page
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        return render(request, "network/following.html", {
            "followUsers": followUsers,
            "posts": posts,
            "page_obj": page_obj,

        })
    else:
        return render(request, "network/index.html")
 
@csrf_exempt   
def edit(request, id):
    if request.method == "POST":
        # Obtain the posts by the user
        data = json.loads(request.body)
        postToEdit = Post.objects.get(pk=id)
        postToEdit.post = data["textPost"]
        postToEdit.save()
        return JsonResponse({"message": "Change succesful", "data": data["textPost"]})

@csrf_exempt
def like(request, id):
    if request.method == "GET":
        currentLikes = Post.objects.get(pk=id)
        likes = currentLikes.likes
        return JsonResponse({"data": likes})
    
    if request.method == "PUT":
        data = json.loads(request.body)
        newLikes = Post.objects.get(pk=id)
        newLikes.likes = data["newNumberLikes"]
        newLikes.save()
        return JsonResponse({"message": "Change succesful", "data": data["newNumberLikes"]})

@csrf_exempt
def liked(request, id):
    if request.method == "GET":
        isItLiked = Post.objects.get(pk=id)
        liked = isItLiked.liked
        unliked = isItLiked.unliked
        return JsonResponse({"message": "liked and unliked boolean obtained", })



