from django.contrib.auth.models import AbstractUser
from django.db import models

import uuid

POST_LIKE_STATE = (("1", "None"), ("2", "Like"))


'''


'''


class User(AbstractUser):
    # field_name = models.ImageField(upload_to=None, height_field=None, width_field=None, max_length=100, **options)

    def __repr__(self):
        return self.username

    def serialize(self):
        return {
            "Username": self.username,
            "Email": self.email
        }


class user_following(models.Model):
    # following functions as the current user here
    main_user = models.ForeignKey(User, null=True,
                                  on_delete=models.CASCADE,
                                  related_name="main_user", verbose_name="Main User")
    # User's current friends
    follower = models.ForeignKey(User, null=True, on_delete=models.CASCADE,
                                 related_name="follower", verbose_name="User Followers")
    # user cannot follow themselves. be careful with this

    def serialize(self):
        return {
            "user_following": self.user_following.username,
            "followers": self.followers.username,
        }
    # def __str__(self):
    #     return "followModel"


class post_class(models.Model):
    post_id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, verbose_name="Post ID")
    post_content = models.CharField(
        max_length=600, verbose_name="Post Content")
    post_owner = models.ForeignKey(
        User, null=True, on_delete=models.CASCADE, related_name="post_owner", verbose_name="Post Owner")
    # post_like = models.CharField(
    #     max_length=50, choices=POST_LIKE_STATE, default="1", verbose_name="Post Like")
    # delete state
    post_state = models.BooleanField(
        default=True, verbose_name="Delete Or Not")
    post_date = models.DateTimeField(
        auto_now_add=True, verbose_name="Post Date")

    # add post like in this model?
    
    def serialize(self):
        return {
            "postid": self.post_id,
            "post_content": self.post_content,
            "post_owner": self.post_owner.username,
            "post_state": self.post_state,
            "post_date": self.post_date.strftime("%b %-d %Y, %-I:%M %p"),
        }
    # def __str__(self):
    #     return {
    #         "id": self.post_id,
    #         "timestamp": self.post_date.strftime("%b %#d %Y, %#I:%M %p"),
    #         "content": self.post_content,
    #         "username": self.post_owner.username,
    #         "state": self.post_state
    #     }


# user to one post like dislike or none
class like(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name="Post Owner")
    post = models.ForeignKey(
        post_class, on_delete=models.CASCADE, verbose_name="Post Content")
    # post_like = models.CharField(
    #     max_length=50, choices=POST_LIKE_STATE, default="1", verbose_name="Post Like")
    
    post_like = models.BooleanField(default=False)
    
    def serialize(self):
        return {
            "user": self.user.username,
            "post": self.post_class.post_content,
            "post_like": self.post_like,
        }
    # def __str__(self):
    #     return {
    #         "id": self.user.username,
    #         "content": self.post.post_content,
    #         "like": self.post_like,
    #     }
