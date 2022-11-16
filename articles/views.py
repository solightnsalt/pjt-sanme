from django.shortcuts import render, redirect
from django.views.decorators.http import require_safe
from .forms import PostForm, CommentForm
from accounts.models import User
from .models import Post, Comment
from django.http import JsonResponse
import json

# Create your views here.
@require_safe
def index(request):
    return render(request, "articles/index.html")


def main(request):
    posts = Post.objects.all()
    context = {
        "posts": posts,
    }
    return render(request, "articles/main.html", context)


def create(request):
    if request.method == "POST":
        post_form = PostForm(request.POST)
        if post_form.is_valid():
            posts = post_form.save(commit=False)
            posts.user = request.user
            posts.save()
            return redirect("articles:board")
    else:
        post_form = PostForm()

    return render(request, "articles/create.html", {"post_form": post_form})


def participate(request, pk):
    # article = get_object_or_404(Article, pk=pk)
    article = Post.objects.get(pk=pk)
    # 만약에 로그인한 유저가 이 글을 좋아요를 눌렀다면,
    # if article.like_users.filter(id=request.user.id).exists():
    if request.user in article.participate.all():
        # 참여하기 삭제하고
        article.participate.remove(request.user)
        # is_participated = False
    else:
        # 참여하기 추가하고
        article.participate.add(request.user)
        # is_participated = True
    # 상세 페이지로 redirect
    return redirect("articles:detail", pk)
    # context = {
    # "is_participated": is_participated,
    # "ParticipateCount": article.participate.count(),
    # }
    # return JsonResponse(context)


def detail(request, pk):
    post = Post.objects.get(pk=pk)
    comment_form = CommentForm()
    comments = Comment.objects.filter(post_id=post).order_by("-updated_at")

    context = {
        "post": post,
        "comment_form": comment_form,
        "comments": comments,
    }

    return render(request, "articles/detail.html", context)


def update(request, pk):
    posts = Post.objects.get(pk=pk)
    if request.method == "POST":
        post_form = PostForm(request.POST, instance=posts)

        if post_form.is_valid():
            post_form.save()

            return redirect("articles:index")
    else:
        post_form = PostForm(instance=posts)

    return render(request, "articles/create.html", {"post_form": post_form})


def delete(request, pk):
    posts = Post.objects.get(pk=pk)
    posts.delete()
    return redirect("articles:index")


def comment(request, pk):
    post = Post.objects.get(pk=pk)
    post_pk = post.pk
    user = request.user.pk
    comment_form = CommentForm(request.POST)

    if comment_form.is_valid():
        comment = comment_form.save(commit=False)
        comment.post = post
        comment.user = request.user
        comment.save()

    temp = Comment.objects.filter(post_id=pk).order_by("-updated_at")
    comment_data = []

    for t in temp:
        t.updated_at = t.updated_at.strftime("%Y-%m-%d %H:%M")
        comment_data.append(
            {
                "user_id": t.user_id,
                "commentPk": t.pk,
                "content": t.content,
                "updated_at": t.updated_at,
                "profile_name": t.user.nickname,
                "profile_img": t.user.profile_pic.url,
            }
        )

    data = {
        "commentData": comment_data,
        "postPk": post_pk,
        "user": user,
    }
    return JsonResponse(data)


def comment_delete(request, pk, comment_pk):
    post_pk = Post.objects.get(pk=pk).pk
    user = request.user.pk
    comment = Comment.objects.get(pk=comment_pk)

    if comment.user == request.user:
        comment.delete()

    temp = Comment.objects.filter(post_id=pk).order_by("-updated_at")
    comment_data = []

    for t in temp:
        t.updated_at = t.updated_at.strftime("%Y-%m-%d %H:%M")
        comment_data.append(
            {
                "user_id": t.user_id,
                "commentPk": t.pk,
                "content": t.content,
                "updated_at": t.updated_at,
                "profile_name": t.user.nickname,
                "profile_img": t.user.profile_pic.url,
            }
        )

    data = {
        "commentData": comment_data,
        "postPk": post_pk,
        "user": user,
    }
    return JsonResponse(data)


def comment_update(request, pk, comment_pk):
    comment = Comment.objects.get(pk=comment_pk)
    comment_username = comment.user.username
    user = request.user.pk
    post_pk = Post.objects.get(pk=pk).pk
    jsonObject = json.loads(request.body)

    if request.method == "POST":
        comment.content = jsonObject.get("content")
        comment.save()

    temp = Comment.objects.filter(post_id=pk).order_by("-updated_at")
    comment_data = []

    for t in temp:
        t.updated_at = t.updated_at.strftime("%Y-%m-%d %H:%M")
        comment_data.append(
            {
                "user_id": t.user_id,
                "commentPk": t.pk,
                "content": t.content,
                "updated_at": t.updated_at,
                "profile_name": t.user.nickname,
                "profile_img": t.user.profile_pic.url,
            }
        )

    data = {
        "commentData": comment_data,
        "comment_pk": comment_pk,
        "comment_username": comment_username,
        "postPk": post_pk,
        "user": user,
    }
    return JsonResponse(data)


def board(request):
    post = Post.objects.all().order_by("-pk")
    context = {
        "post": post,
    }
    return render(request, "articles/board.html", context)


def recommend(request, pk):
    user_data = User.objects.all(pk=pk)
    if request.user == user_data:
        print(user_data)
    return render(request, pk)
