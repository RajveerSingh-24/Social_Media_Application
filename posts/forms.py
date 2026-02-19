from django import forms
from .models import Post
from .models import Comment


class PostCreateForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["image", "caption"]
        widgets = {
            "caption": forms.Textarea(attrs={
                "rows": 3,
                "placeholder": "Write a caption..."
            })
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["text"]
        widgets = {
            "text": forms.TextInput(
                attrs={
                    "placeholder": "Add a comment...",
                    "class": "comment-input"
                }
            )
        }