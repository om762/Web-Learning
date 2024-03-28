from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
def index(request):
    # return HttpResponse("Hello, World!")  # For just printing simple text
    return render(request, "hello/index.html")


def om(request):
    return HttpResponse("Hello Omprakash Rawat. Nice to meet you sir!")

def greet(request, name):
    # return HttpResponse(f"Hello, {name.capitalize()}!") # For just printing simple text
    return render(request, "hello/greet.html", {
        "name":name.capitalize()
    })