from django.contrib.auth import get_user_model
from django.db import models
from django.contrib.auth.models import AbstractUser
from taggit.managers import TaggableManager


class User(AbstractUser):

    def __str__(self):
        return self.username


class Post(models.Model):
    owner = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name="posts"
    )
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=255, default="")
    content = models.TextField()
    created_time = models.DateTimeField(auto_now_add=True)
    tags = TaggableManager()

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["-created_time"]


class Comment(models.Model):
    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name="comments"
    )
    post = models.ForeignKey(
        "blog_app.Post",
        on_delete=models.CASCADE,
        related_name="comments"
    )
    created_time = models.DateTimeField(auto_now_add=True)
    content = models.TextField()

    class Meta:
        verbose_name = "comment"
        verbose_name_plural = "comments"

    def __str__(self):
        return f"{self.content} ({self.user} - {self.post})"


class Like(models.Model):
    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name="likes"
    )
    post = models.ForeignKey(
        "blog_app.Post",
        on_delete=models.CASCADE,
        related_name="likes"
    )

    class Meta:
        unique_together = ("user", "post")

    def __str__(self):
        return f"{self.user} liked {self.post}"
