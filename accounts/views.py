from django.shortcuts import render, redirect
from django.views.decorators.http import require_safe
from .forms import CustomUserCreationForm
from django.contrib.auth import login as auth_login


# Create your views here.
@require_safe
def index(request):
    return render(request, "accounts/index.html")


def signup(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():  # 폼이 유효하면
            user = form.save()
            auth_login(request, user)
            return redirect("articles:index")
    else:
        form = CustomUserCreationForm()
    context = {"form": form}
    return render(request, "accounts/signup.html", context)
