from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.views.decorators.http import require_safe
from .forms import CustomUserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import get_user_model
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.contrib import messages


# Create your views here.
@require_safe
def login(request):
    if request.user.is_anonymous:
        if request.method == "POST":
            login_form = AuthenticationForm(request, data=request.POST)
            if login_form.is_valid():
                auth_login(request, login_form.get_user())
                return redirect("articles:detail")
        else:
            login_form = AuthenticationForm()

        context = {
            "login_form": login_form,
        }
        return render(request, "accounts/login.html", context)
    else:
        return HttpResponseRedirect("/login")


def logout(request):
    auth_logout(request)
    return redirect("accounts:login")


def signup(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()  # ModelForm의 save메소드의 리턴값은 해당 모델의 인스턴스다
            auth_login(request, user)  # 로그인
            return redirect("articles:index")
    else:
        form = CustomUserCreationForm()
    context = {
        "form": form,
    }
    return render(request, "accounts/signup.html", context)


def detail(request, pk):
    user = get_user_model().objects.get(pk=pk)
    context = {
        "user": user,
    }
    return render(request, "accounts/detail.html", context)
