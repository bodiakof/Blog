from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin


from blog_app.models import User, Post, Comment


@admin.register(User)
class CustomUserAdmin(BaseUserAdmin):
    search_fields = ["username", "email"]
    list_display = ["username", "email", "first_name", "last_name"]


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    search_fields = ["title", "owner__username"]
    list_display = ["title", "owner", "created_time"]
    filter_horizontal = ("tags",)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    search_fields = ["content", "post__title", "user__username"]
    list_display = ["user", "post", "content", "created_time"]
