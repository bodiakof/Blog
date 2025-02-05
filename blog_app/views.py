from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import QuerySet
from django.forms import ModelForm
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views import generic

from .forms import CommentForm
from .models import Post, Comment


class PostListView(generic.ListView):
    model = Post
    queryset = Post.objects.select_related("owner")
    paginate_by = 5
    template_name = "blog/post_list.html"


class UserPostListView(generic.ListView):
    model = Post
    paginate_by = 5
    template_name = "blog/post_list.html"

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        author_id = self.kwargs.get("user_pk")
        context["author_id"] = author_id
        return context

    def get_queryset(self) -> QuerySet:
        author_id = self.kwargs.get("user_pk")
        return Post.objects.select_related("owner").filter(owner=author_id)


class PostDetailView(generic.DetailView):
    model = Post
    queryset = (
        Post.objects.prefetch_related("comments__user")
    )
    template_name = "blog/post_detail.html"

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        context["form"] = CommentForm()
        return context


class PostCreateView(LoginRequiredMixin, generic.CreateView):
    model = Post
    fields = ["title", "description", "content"]
    success_url = reverse_lazy("blog:post-list")
    template_name = "blog/post_form.html"

    def form_valid(self, form: ModelForm) -> HttpResponse:
        post = form.save(commit=False)
        post.owner = self.request.user
        post.save()
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Post
    fields = ["title", "description", "content"]
    template_name = "blog/post_form.html"

    def get_success_url(self):
        return reverse_lazy("blog:post-detail", kwargs={"pk": self.object.pk})


class PostDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Post
    success_url = reverse_lazy("blog:post-list")
    template_name = "blog/post_confirm_delete.html"


class CommentListView(generic.ListView):
    model = Comment
    template_name = "blog/comment_list.html"

    def get_queryset(self):
        post_id = self.kwargs.get("pk")
        return Comment.objects.filter(post=post_id)


class CommentCreateView(LoginRequiredMixin, generic.CreateView):
    model = Comment
    fields = ["content"]
    template_name = "blog/comment_form.html"

    def form_valid(self, form: ModelForm) -> HttpResponse:
        post_id = self.kwargs.get("pk")
        comment = form.save(commit=False)
        comment.user = self.request.user
        comment.post = Post.objects.get(pk=post_id)
        comment.save()
        return super().form_valid(form)

    def get_success_url(self) -> str:
        return reverse_lazy(
            "blog:comment-list",
            kwargs={"pk": self.object.post.pk}
        )


class CommentUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Comment
    fields = ["content"]
    template_name = "blog/comment_list.html"

    def get_success_url(self) -> str:
        return reverse_lazy(
            "blog:comment-list",
            kwargs={"pk": self.object.post.pk}
        )


class CommentDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Comment
    template_name = "blog/comment_list.html"

    def get_success_url(self) -> str:
        return reverse_lazy(
            "blog:comment-list",
            kwargs={"pk": self.object.post.pk}
        )