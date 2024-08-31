from django.shortcuts import render
from django.http import JsonResponse

# Create your views here.
def index(request):
    return render(request, "index.html")

def posts(request):
    start = int(request.GET.get("start") or 0)
    end = int(request.GET.get("end") or (start + 10))
    
    new_posts = []
    for i in range(start, end):
        new_posts.append(f"Post #{i}")
    
    return JsonResponse({
        "posts":new_posts
    })
