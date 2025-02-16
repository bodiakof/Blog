from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import QuerySet
from django.forms import ModelForm
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views import generic, View
from django.views.generic import CreateView

from taggit.models import Tag

from blog_app.forms import CommentForm, CustomUserCreationForm
from blog_app.models import Post, Comment, Like


class RegisterView(CreateView):
    form_class = CustomUserCreationForm
    template_name = "registration/register.html"
    success_url = reverse_lazy("blog:home")


class LikePostView(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        post = get_object_or_404(Post, pk=pk)
        like, created = Like.objects.get_or_create(
            user=request.user,
            post=post
        )

        if not created:
            like.delete()

        return HttpResponseRedirect(
            reverse("blog:post-detail",
                    kwargs={"pk": pk})
        )


class PostListView(generic.ListView):
    model = Post
    queryset = Post.objects.select_related("owner")
    paginate_by = 3
    template_name = "blog/post_list.html"


class UserPostListView(generic.ListView):
    model = Post
    paginate_by = 3
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
        Post.objects.prefetch_related("comments__user", "likes", "tags")
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

        self.object = comment

        return redirect(self.get_success_url())

    def get_success_url(self) -> str:
        return reverse_lazy("blog:post-detail", kwargs={"pk": self.object.post.pk})


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


class TaggedPostListView(generic.ListView):
    model = Post
    template_name = "blog/post_list.html"
    context_object_name = "post_list"

    def get_queryset(self) -> QuerySet:
        tag_slug = self.kwargs.get("slug")
        tag = get_object_or_404(Tag, slug=tag_slug)
        return Post.objects.filter(tags__in=[tag])

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        context["tag"] = get_object_or_404(Tag, slug=self.kwargs.get("slug"))
        return context
