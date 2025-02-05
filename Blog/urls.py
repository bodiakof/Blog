from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from blog_app.views import RegisterView, PostListView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("register/", RegisterView.as_view(), name="register"),
    path("accounts/", include("django.contrib.auth.urls")),
    path("", include("blog_app.urls", namespace="blog")),
    path("", PostListView.as_view(), name="home"),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
