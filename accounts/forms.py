from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model


class DateInput(forms.DateInput):
    input_type = "Date"


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = (
            "profile_pic",
            "username",
            "email",
            "nickname",
            "contact",
            "mbti",
            "age",
            "address",
            "gender",
            "manner",
            "smoking",
            "pet",
            "agree",
        )
        widgets = {
            "age": DateInput(),
        }
