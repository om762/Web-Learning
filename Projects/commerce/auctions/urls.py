from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("listing/<str:item_id>", views.listing_detail, name="listing_detail"),
    path("create_listing", views.create_listing, name="create_listing"),
    path("category", views.categories, name="categories"),
    path("category/<str:type>", views.category, name="category"),
    path("category", views.categories, name="watchlist"),
    # path("add_bid", views.bid, name="bid"),
    path("add_comment", views.add_comment, name="add_comment"),
]
