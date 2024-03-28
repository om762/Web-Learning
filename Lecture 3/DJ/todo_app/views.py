from django.shortcuts import render, redirect
from django import forms
from django.http import HttpResponseRedirect
from django.urls import reverse

class NewTaskForm(forms.Form):
    task = forms.CharField(label="New Task")

# todo_list = []      # May create a global list for all the user

# Create your views here.
def index(request):
    if "todo_list" not in request.session:
        request.session["todo_list"] = []
    return render(request, "todo_app/index.html", {
        "todo_list": request.session["todo_list"]
    })

# Add method with using django forms
# def add(request):
#     if request.method == "POST":
#         form = NewTaskForm(request.POST)
#         if form.is_valid():
#             task = form.cleaned_data["task"]
#             request.session["todo_list"] += [task]
#             return HttpResponseRedirect(reverse("todo_app:index"))
        
#         else:
#             return render(request, "todo_app/add.html", {
#                 "form":form
#             })
    
#     return render(request, "todo_app/add.html", {
#         "form": NewTaskForm()
#     })

# Add method without using django forms
def add(request):
    if request.method == "POST":
        task = request.POST.get("task", "")
        if task:
            request.session["todo_list"] += [task]
            return redirect("todo_app:index")
    
    return render(request, "todo_app/add.html")