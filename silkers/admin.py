from django.contrib import admin
from models import UserProfile


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['shoe_size', 'dress_size']

admin.site.register(UserProfile, UserProfileAdmin)
