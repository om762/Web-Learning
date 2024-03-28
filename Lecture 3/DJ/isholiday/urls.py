from django.urls import path
from . import views

app_name = "isholiday"

urlpatterns = [
    path("", views.index, name="index")
]
