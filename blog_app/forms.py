from django import forms

from blog_app.models import Comment


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