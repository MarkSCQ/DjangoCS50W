# Author:   https://github.com/MarkSCQ/

from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required

import json
from django.http import JsonResponse

from .models import user_following, post_class, like

import os
from django.conf import settings


def index(request):
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


@csrf_exempt
@login_required
def makeposts(request):
    # use this function to store the post content to models
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)
    data = json.loads(request.body)

    dk = data.get("postcontent")
    dv = data.get("postcontent")

    print(type(data))
    current_user = request.user
    post_content = data.get("postcontent")

    cur_post = post_class(post_owner=current_user, post_content=post_content)
    cur_post.save()

    return JsonResponse({"message": f"Got it! {dk}"}, status=201)


def getAllPosts(request):

    PostDic = {}
    current_user = str(request.user)

    posts_mine = post_class.objects.all().filter(
        post_owner=User.objects.all().get(username=current_user).id)

    post_like_mine = []

    posts_me = [i.serialize() for i in posts_mine]
    for i in range(len(posts_mine)):
        PostDic[posts_mine[i].post_owner] = posts_mine[i].post_content

    myFollowing = [i.main_user.username for i in user_following.objects.all().filter(
        follower=User.objects.all().get(username=current_user).id)]

    # ANCHOR put get likes here

    post_records = []

    posts_following = []

    for i in myFollowing:
        post_records.append(post_class.objects.all().filter(
            post_owner=User.objects.all().get(username=i)))
    for i in post_records:
        for j in i:
            posts_following.append(j.serialize())
    posts_all = posts_me + posts_following

    newrecords = sorted(posts_all, key=lambda i: (
        i["post_date"]), reverse=True)

    for i in newrecords:
        i['post_likers'] = [str(i.user.username) for i in like.objects.filter(
            post=post_class.objects.get(post_id=i['postid']), post_like=True)]
    # current like or not
    for i in newrecords:
        # likelist = like.objects.get(post = post_class.objects.get(post_id = i["postid"]))
        if (current_user in i['post_likers']):
            i['curr_like'] = True
        else:
            i['curr_like'] = False

    return JsonResponse(newrecords, safe=False)


def getProfile_mine(request):

    current_user = request.user
    # following
    following = [i.main_user.username for i in user_following.objects.filter(
        follower=User.objects.get(username=current_user).id)]

    # follower
    follower = [i.follower.username for i in user_following.objects.filter(
        main_user=User.objects.get(username=current_user).id)]
    # posts of mine
    posts_mine = [i.serialize() for i in post_class.objects.filter(
        post_owner=User.objects.get(username=current_user).id)]
    # email
    myEmail = User.objects.get(username=current_user).email

    newrecords = sorted(posts_mine, key=lambda i: (
        i["post_date"]), reverse=True)

    # ANCHOR put get likes here

    myProfileDic = {
        "user": str(current_user),
        "following": following,
        "followers": follower,
        "postmine": newrecords,
        "myemail": myEmail
    }

    return JsonResponse(myProfileDic, safe=False)


def getProfile(request, username):

    current_user = username
    # following
    following = [i.main_user.username for i in user_following.objects.filter(
        follower=User.objects.get(username=current_user).id)]

    # follower
    follower = [i.follower.username for i in user_following.objects.filter(
        main_user=User.objects.get(username=current_user).id)]
    # posts of mine
    posts_mine = [i.serialize() for i in post_class.objects.filter(
        post_owner=User.objects.get(username=current_user).id)]

    myProfileDic = {
        "user": str(current_user),
        "following": following,
        "followers": follower,
        "postmine": posts_mine
    }

    return JsonResponse(myProfileDic, safe=False)


@csrf_exempt
@login_required
def postupdate(request):

    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)
    data = json.loads(request.body)

    current_user = request.user
    post_content = str(data.get("postcontent"))

    cur_post = post_class(post_owner=current_user, post_content=post_content)
    cur_post.save()

    postID = data.get("postID")
    postGET = post_class.objects.get(post_id=postID)
    postGET.delete()

    return JsonResponse({"message": f"{postID}"}, status=201)


@csrf_exempt
@login_required
def postLike(request, postid):
    # get post state and change the postid by using fucking put
    # likeornot = request.get("likestate")
    current_user = str(request.user)
    data = json.loads(request.body)
    likestate = data.get("likestate")
    # if exist,
    #   change true to false
    #   change false to true
    # if not exist:
    #   create a new one and make it true
    tp = likestate
    try:
        postget = like.objects.get(post=post_class.objects.get(
            post_id=postid), user=User.objects.get(username=current_user))
        postget.post_like = likestate
        tp = postget.post_like
        postget.save()
    except like.DoesNotExist:
        like_instance = like(post=post_class.objects.get(
            post_id=postid), user=User.objects.get(username=current_user))
        like_instance.post_like = likestate
        tp = like_instance.post_like
        like_instance.save()

    return JsonResponse({"current_state": tp}, status=201)


'''
我从去年辞帝京，谪居卧病浔阳城。
浔阳地僻无音乐，终岁不闻丝竹声。
住近湓江地低湿，黄芦苦竹绕宅生。
其间旦暮闻何物？杜鹃啼血猿哀鸣。
春江花朝秋月夜，往往取酒还独倾。
岂无山歌与村笛？呕哑嘲哳难为听。
今夜闻君琵琶语，如听仙乐耳暂明。
'''
