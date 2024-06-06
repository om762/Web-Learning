from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path('profile/', views.profile_view, name='profile'),
    path('all_listings', views.all_listings, name="all_listings"),
    path("listing/<str:item_id>", views.listing_detail, name="listing_detail"),
    path("create_listing", views.create_listing, name="create_listing"),
    path("category", views.categories, name="categories"),
    path("category/<str:type>", views.category, name="category"),
    path("add_to_watchlist", views.add_to_watchlist, name="add_to_watchlist"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("close_bidding", views.close_bidding, name="close_bidding"),
    path("add_comment", views.add_comment, name="add_comment"),
    path("<str:invalid_path>", views.page_not_found, name="page_not_found")
]
