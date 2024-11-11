from django.shortcuts import render
from django.http import JsonResponse
from time import sleep

# Create your views here.
def index(request):
    return render(request, "index.html")

def posts(request):
    start = int(request.GET.get("start") or 1)
    end = int(request.GET.get("end") or 10)
    
    sleep(0.5)
    
    new_posts = []
    for i in range(start, end + 1):
        new_posts.append(f"Post #{i}")
    
    return JsonResponse({
        "posts":new_posts
    })
