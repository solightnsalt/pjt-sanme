from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.views.decorators.http import require_safe
from .forms import CustomUserCreationForm
from .forms import CustomUserChangeForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import get_user_model
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.http import JsonResponse

# Create your views here.


def login(request):
    if request.user.is_anonymous:
        if request.method == "POST":
            login_form = AuthenticationForm(request, data=request.POST)
            if login_form.is_valid():
                auth_login(request, login_form.get_user())
                return redirect("articles:index")
        else:
            login_form = AuthenticationForm()

        context = {
            "login_form": login_form,
        }
        return render(request, "accounts/login.html", context)
    else:
        return HttpResponseRedirect("/")


def logout(request):
    auth_logout(request)
    return redirect("accounts:login")


def signup(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()  # ModelForm의 save메소드의 리턴값은 해당 모델의 인스턴스다
            auth_login(request, user)  # 로그인
            return redirect("articles:main")
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


@login_required
def update(request, pk):
    user_info = get_user_model().objects.get(pk=pk)
    # 요청한 유저가 로그인한 해당 유저인 경우
    if request.method == "POST":
        user_form = CustomUserChangeForm(
            request.POST, request.FILES, instance=request.user
        )
        # 유저폼 유효성 확인
        if user_form.is_valid():
            user_form.save()
            return redirect("accounts:detail", user_info.pk)
    else:
        user_form = CustomUserChangeForm(instance=request.user)
    context = {"user_form": user_form}
    return render(request, "accounts/update.html", context)


# def follow(request, pk):
#     accounts = get_user_model().objects.get(pk=pk)
#     if request.user == accounts:
#         return redirect("accounts:detail", pk)
#     if request.user in accounts.followers.all():
#         accounts.followers.remove(request.user)
#     else:
#         accounts.followers.add(request.user)
#     return redirect("accounts:detail", pk)


# 팔로우
# @login_required
# def follow(request, pk):
#     if request.user.is_authenticated:
#         User = get_user_model()
#         me = request.user
#         you = User.objects.get(pk=pk)
#         if me != you:
#             if you.followers.filter(pk=me.pk).exists():
#                 you.followers.remove(me)
#                 you.manner -= 0.2
#                 you.save()
#                 is_followed = False
#             else:
#                 you.followers.add(me)
#                 you.manner += 0.2
#                 you.save()
#                 is_followed = True
#             context = {
#                 "is_followed": is_followed,
#                 "followers_count": you.followers.count(),
#                 "followings_count": you.followings.count(),
#             }
#             return JsonResponse(context)
#         return redirect("accounts:detail", you.username)
#     return redirect("accounts:login")
@login_required
def follow(request, pk):
    accounts = get_user_model().objects.get(pk=pk)
    if request.user == accounts:
        return redirect("accounts:detail", pk)
    if request.user in accounts.followers.all():
        accounts.followers.remove(request.user)
        accounts.manner_point -= 0.2
        accounts.save()
    else:
        accounts.followers.add(request.user)
        accounts.manner_point += 0.2
        accounts.save()
    # 상세 페이지로 redirect
    return redirect("accounts:detail", pk)


def delete(request):
    request.user.delete()
    auth_logout(request)
    return redirect("accounts:index")
