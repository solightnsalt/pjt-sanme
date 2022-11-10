from django import forms
from .models import Post

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            "title",
            "day_time",
            "park_address",
            "pet",
            "content",
        ]