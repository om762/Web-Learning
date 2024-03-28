from django.urls import path
from . import views

app_name = "square"

urlpatterns = [
    path('', views.index, name="index"),
    path('<int:num>', views.square, name="square")
]
