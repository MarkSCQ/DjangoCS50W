
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("makeposts", views.makeposts, name="makeposts"),
    path("getAllPosts", views.getAllPosts, name="getAllPosts"),
    path("getProfile_mine/", views.getProfile_mine, name="getProfile_mine"),
    path("getProfile/<str:username>", views.getProfile, name="getProfile"),
    path("postLike/<str:postid>", views.postLike, name="postLike"),
    path("postupdate", views.postupdate, name="postupdate"),
    
    # path("postLike/<str:postid>", views.postLike, name="postLike"),

]
