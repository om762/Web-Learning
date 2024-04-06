from .util import *
from django.shortcuts import render, redirect
from django.http import HttpResponse
import markdown2 as md
import random


def index(request):
    if request.method == "GET":
        query = request.GET.get("q", "")
        if query:
            if query in list_entries():
                return redirect("entry", TITLE=query)
    return render(request, "encyclopedia/index.html", {
        "entries": list_entries()
    })


def entry(request, TITLE):
    content = get_entry(TITLE)
    if content:
        content = md.markdown(content)
        return render(request, "encyclopedia/entry.html",{
            "TITLE":TITLE,
            "content":content
        })
    else:
        return render(request, "encyclopedia/404.html", {
            "TITLE":TITLE
        })

def search(request):
    query = request.GET.get("q", "").lower()
    entries = list_entries()
    matching_entries = [entry for entry in entries if query in entry.lower()]
    if matching_entries:
        if query in [entry.lower() for entry in entries]:
            return redirect("entry", TITLE=query)
        else:
            return render(request, "encyclopedia/search_results.html", {
                "query": query,
                "entries": matching_entries
            })
    else:
        return render(request, "encyclopedia/search_results.html", {
            "query": query,
            "entries": []
        })

def new(request):
    if request.method == "POST":
        title = request.POST.get("title", "")
        content = request.POST.get("markdown", "")
        
        if title not in list_entries():
            save_entry(title=title, content=content)
            title = ""
            content = ""
            return render(request, "encyclopedia/new.html", {
                "status" : "success",
                "title" : title,
                "content" : content
            })
        else:
            return render(request, "encyclopedia/new.html", {
                "status" : "failed",
                "title" : title,
                "content" : content
            })
    else:
        return render(request, "encyclopedia/new.html", {
                    "status" : "new",
                    "title" : "",
                    "content" : ""
                })

def edit(request, TITLE):
    if request.method == "POST":
        content = request.POST.get("markdown", "")
        save_entry(TITLE, content)
        return redirect("entry", TITLE=TITLE)
    content = get_entry(TITLE)
    return render(request, "encyclopedia/edit.html", {
        "content" : content,
        "TITLE" : TITLE
    })

def random_page(request):
    title = random.choice(list_entries())
    return redirect("entry", TITLE=title)
