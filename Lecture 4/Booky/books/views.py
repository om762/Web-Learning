import random
from django.shortcuts import render
from .models import *



# Create your views here.
def index(request):
    random_books = Book.objects.filter(pk__in=random.sample(range(Book.objects.count()), 6))
    return render(request, "books/index.html", {
        "random_books" : random_books
    }) 
