from django.urls import path
from . import views

app_name = "hello"

urlpatterns = [
    path("", views.index, name="index"),
    path("om/", views.om, name="om"),
    path("<str:name>", views.greet, name="greet")
]
