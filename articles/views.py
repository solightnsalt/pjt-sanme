from django.shortcuts import render,redirect
from django.views.decorators.http import require_safe
from .forms import PostForm
from .models import Post


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
            return redirect("articles:index")
    else :
        post_form = PostForm()
        
    
    return render(request, "articles/create.html",{"post_form" : post_form})

def detail(request,pk):
    post = Post.objects.get(pk=pk)
    context = {
        "post":post,
    }
    
    return render(request,"articles/detail.html",context)