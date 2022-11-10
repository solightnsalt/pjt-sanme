from django.shortcuts import render,redirect
from django.views.decorators.http import require_safe
from .forms import PostForm, CommentForm
from .models import Post, Comment


# Create your views here.
@require_safe
def index(request):
    return render(request, "articles/index.html")

def create(request):
    if request.method == 'POST':
        post_form = PostForm(request.POST)
        if post_form.is_valid():
            posts = post_form.save(commit=False)
            posts.user = request.user
            posts.save()
            return redirect("articles:postall")
    else :
        post_form = PostForm()
        
    
    return render(request, "articles/create.html",{"post_form" : post_form})

def detail(request,pk):
    post = Post.objects.get(pk=pk)
    comment_form = CommentForm()
    comments = Comment.objects.all().order_by('-updated_at')

    context = {
        "post":post,
        "comment_form": comment_form,
        "comments": comments,
    }
    
    return render(request,"articles/detail.html",context)


def update(request,pk):
    posts = Post.objects.get(pk=pk)
    if request.method == 'POST':
        post_form = PostForm(request.POST, instance=posts)
        
        if post_form.is_valid():
            post_form.save()
            
            return redirect("articles:index")
    else:
        post_form = PostForm(instance=posts)
    
    
    return render(request,"articles/create.html",{"post_form":post_form})


def delete(request, pk):
    posts = Post.objects.get(pk=pk)
    posts.delete()
    return redirect("articles:index") 

    
def comment(request, pk):
    post = Post.objects.get(pk=pk)
    
    if request.method == "POST":
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment_form.save(commit=False)
            comment.post = post
            comment.user = request.user
            comment.save()
    
    return redirect('articles:detail', post.pk)

def postall(request):
    post = Post.objects.all().order_by("-pk")
    context = {
        "post": post,
    }
    return render(request, "articles/postall.html", context)