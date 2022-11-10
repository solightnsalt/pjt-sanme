from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = (
            "profile_pic",
            "username",
            "password",
            "email",
            "nickname",
            "contact",
            "mbti",
            "address",
            "age",
            "gender",
            "manner",
            "smoking",
            "pet",
            "agree",
        )
