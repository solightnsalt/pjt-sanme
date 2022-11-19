from django.shortcuts import render, redirect
from django.views.decorators.http import require_safe
from .forms import PostForm, CommentForm
from accounts.models import User
from maps.models import Map
from .models import Post, Comment, Search
from django.db.models import Q
from django.core.paginator import Paginator
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
            posts.park_address = Map.objects.get(pk=request.GET.get("park", ""))
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


# 취소
def delete_participate(request, pk):
    post = Post.objects.get(pk=pk)
    post.participate.delete(request.user)
    return redirect("articles:detail", pk)


def detail(request, pk):
    post = Post.objects.get(pk=pk)
    comment_form = CommentForm()
    comments = Comment.objects.filter(post_id=post).order_by("-updated_at")
    post.hit += 1
    post.save()
    context = {
        "post": post,
        "comment_form": comment_form,
        "comments": comments,
    }

    return render(request, "articles/detail.html", context)


def update(request, pk):
    posts = Post.objects.get(pk=pk)
    if request.user == posts.user:
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


import random


def recommend(request, pk):
    # mbti 별 잘 맞는 유형
    mbti_info = {
        "ENTJ": ["ISFP", "INFP", "ESFP", "ESTP"],
        "ENTP": ["ISFJ", "ISTJ", "ENTP", "ESTJ"],
        "INTJ": ["ESFP", "ESTP", "ISFP", "INTP"],
        "INTP": ["ESFP", "ESTP", "ISFP", "INFP"],
        "ESTJ": ["INFP", "ISFP", "INTP", "ENTP"],
        "ESFJ": ["INTP", "ISTP", "ENTP", "ENFP"],
        "ISTJ": ["ENFP", "ENTP", "ISFP", "INFP"],
        "ISFJ": ["ENTP", "ENFP", "INTP", "ISTP"],
        "ENFJ": ["ISTP", "INTP", "ESTP", "ESFP"],
        "ENFP": ["ISTJ", "ISTJ", "ESFJ", "ESTJ"],
        "INFJ": ["ESTP", "ESFP", "ISTP", "INTP"],
        "INFP": ["ESTJ", "ENTJ", "INTJ", "ISTJ"],
        "ESTP": ["INFJ", "INTJ", "ENFJ", "ENTJ"],
        "ESFP": ["INTJ", "INFJ", "ENTJ", "ENFJ"],
        "ISTP": ["ENFJ", "ESFJ", "INFJ", "ISFJ"],
        "ISFP": ["ENTJ", "ESTJ", "INTJ", "ISTJ"],
    }
    # mbti에 따른 유저 3명 추출하기
    # 유저 정보를 가져옴
    my_data = User.objects.get(pk=pk)
    # 유저의 mbti
    my_mbti = my_data.mbti
    # 해당 유저와 잘 맞는 유저 리스트
    matched_user = []
    # mbti 키, 값
    try:
        for mbti_key, mbti_value in mbti_info.items():
            # 유저의 mbti가 키에 있으면
            if my_mbti == mbti_key:
                # 값에 해당하는 유저를 골라냄
                for info in mbti_value:
                    user_data = User.objects.filter(mbti=info)
                    # 유저 데이터가 하나의 mbti에 2개 이상일 경우
                    if len(user_data) <= 2:
                        # 1개만 랜덤으로 추려냄
                        user_data = random.choice(user_data)
                    matched_user.append(user_data)
        # 결과적으로 3개의 유저 데이터 도출
        matched_user = random.sample(matched_user, 3)
    except IndexError:
        print("해당하는 유저가 없습니다")
    except ValueError:
        print("데이터가 없습니다.")

    # 매너유저 3명
    hot_user = User.objects.all().order_by("-manner_point")[:3]
    print(hot_user)
    context = {
        "my_mbti": my_mbti,
        "matched_user": matched_user,
        "hot_user": hot_user,
    }

    return render(request, "articles/main.html", context)


def search(request):
    popular_list = {}
    if request.method == "GET":
        search = request.GET.get("searched", "")
        sort = request.GET.get("sorted", "")

        if not search.isdigit() and not search == "":
            # 검색받을 항목
            if Post.objects.filter(
                Q(title__icontains=search)
                | Q(content__icontains=search)
                | Q(day__icontains=search)
            ):
                popular_list[search] = popular_list.get(search, 0) + 1

        # 인기순
        for k, v in sorted(popular_list.items(), key=lambda x: -x[1]):
            if Search.objects.filter(title=k):
                s = Search.objects.get(title=k)
                s.count += 1
                s.save()
            else:
                s = Search(title=k, count=v)
                s.save()
        popular = Search.objects.order_by("-count")[:10]

        search_list = Post.objects.filter(
            Q(title__icontains=search)
            | Q(content__icontains=search)
            | Q(day__icontains=search)
        )

        if search:
            if search_list:
                pass

            if sort == "recent":
                search_list = search_list.order_by("-updated_at")
                sort = "recent"
                print(search_list)

            page = int(request.GET.get("p", 1))
            pagenator = Paginator(search_list, 5)
            boards = pagenator.get_page(page)

            print(search)
            print(boards)
            print(search_list)
            print(popular)
            return render(
                request,
                "articles/search.html",
                {
                    "search": search,
                    "boards": boards,
                    "search_list": search_list,
                    "popular": popular,
                    "sort": sort,
                },
            )
        else:
            k = "검색 결과가 없습니다 다시 검색해주세요"
            context = {"v": k}
            return render(request, "articles/searchfail.html", context)


def searchfail(request):
    popular_search = Search.objects.order_by("-count")[:10]

    context = {
        "popular": popular_search,
    }
    return render(request, "articles/searchfail.html", context)


def support(request):
    return render(request, "articles/support.html")
