from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.views.decorators.http import require_safe
from .forms import CustomUserCreationForm
from django.contrib.auth import login as auth_login


# Create your views here.
@require_safe
def index(request):
    return render(request, "accounts/index.html")


def signup(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()  # ModelForm의 save메소드의 리턴값은 해당 모델의 인스턴스다
            auth_login(request, user)  # 로그인
            return redirect("accounts:index")
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
