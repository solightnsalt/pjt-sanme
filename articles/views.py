from django.shortcuts import render
from django.views.decorators.http import require_safe


# Create your views here.
@require_safe
def index(request):
    return render(request, "articles/index.html")
