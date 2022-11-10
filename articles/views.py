from django.shortcuts import render, redirect
from django.views.decorators.http import require_safe
from .forms import CommentForm
from .models import Post


# Create your views here.
@require_safe
def index(request):
    return render(request, "articles/index.html")

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
