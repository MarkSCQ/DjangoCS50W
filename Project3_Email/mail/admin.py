from django.contrib import admin

from .models import User,Email
from django.contrib.auth.admin import UserAdmin


class UserAD(UserAdmin):
    pass

class EmailAD(admin.ModelAdmin):
    pass
# Register your models here.
admin.site.register(User, UserAD)
admin.site.register(Email, EmailAD)
