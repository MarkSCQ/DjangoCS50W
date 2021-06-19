from django.contrib import admin
from .models import user_following, post_class, like, User

# Register your models here.


@admin.register(User)
class UserAdmin(admin.ModelAdmin):

    pass


@admin.register(user_following)
class UserFollowingAdmin(admin.ModelAdmin):
    list_display = ("main_user", "follower")
    ordering = ("main_user", "follower")
    pass


@admin.register(post_class)
class PostClassAdmin(admin.ModelAdmin):
    list_display = ("post_owner", "post_content", "post_state", "post_date")
    ordering = ("post_owner", "post_date")

    pass


@admin.register(like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ("user", "post",
                    "post_like")

    pass
