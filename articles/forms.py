from django import forms
from .models import Post, Comment


class DateInput(forms.DateInput):
    input_type = "date"


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            "title",
            "day",
            "time",
            "park_address",
            "pet",
            "participate_people",
            "thumbnail",
            "content",
        ]
        widgets = {
            "day": DateInput(),
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["content"]
