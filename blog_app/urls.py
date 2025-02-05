from django.urls import path

from blog_app.views import (
    PostListView,
    PostDetailView,
    PostCreateView,
    PostUpdateView,
    PostDeleteView,
    UserPostListView,
    CommentListView,
    CommentCreateView,
    CommentUpdateView,
    CommentDeleteView,
    LikePostView,
)

app_name = "blog"

urlpatterns = [
    path("", PostListView.as_view(), name="home"),
    path("posts/", PostListView.as_view(), name="post-list"),
    path("posts/<int:pk>/", PostDetailView.as_view(), name="post-detail"),
    path(
        "posts/user/<int:user_pk>/",
        UserPostListView.as_view(),
        name="user-post-list"
    ),
    path(
        "posts/create/",
        PostCreateView.as_view(),
        name="post-create"
    ),
    path(
        "posts/<int:pk>/update/",
        PostUpdateView.as_view(),
        name="post-update"
    ),
    path(
        "posts/<int:pk>/delete/",
        PostDeleteView.as_view(),
        name="post-delete"
    ),
    path(
        "posts/<int:pk>/comments/",
        CommentListView.as_view(),
        name="comment-list"
    ),
    path(
        "posts/<int:pk>/comments/create/",
        CommentCreateView.as_view(),
        name="comment-create",
    ),
    path(
        "posts/comments/<int:pk>/update/",
        CommentUpdateView.as_view(),
        name="comment-update",
    ),
    path(
        "post/comments/<int:pk>/delete/",
        CommentDeleteView.as_view(),
        name="comment-delete",
    ),
    path("post/<int:pk>/like/", LikePostView.as_view(), name="post-like")
]
