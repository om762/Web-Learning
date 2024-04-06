from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki", views.index, name="wiki"),
    path("wiki/<str:TITLE>", views.entry, name="entry"),
    path("search", views.search, name="search"),
    path("new", views.new, name="new"),
    path("edit/<str:TITLE>", views.edit, name="edit"),
    path("random_page", views.random_page, name="random_page")
]
