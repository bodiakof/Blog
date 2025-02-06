from django import forms
from django.contrib.auth.forms import UserCreationForm

from blog_app.models import Comment, User


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["content"]
        labels = {"content": ""}
        widgets = {
            "content": forms.Textarea(
                attrs={"placeholder": "Enter new comment here", "rows": 3}
            )
        }
