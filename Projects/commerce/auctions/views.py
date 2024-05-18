from django.contrib.auth import authenticate, login, logout
from django.db.models import F
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import *


def index(request):
        active_listings = Listing.objects.filter(active=True).order_by(F('created_at').desc())
        return render(request, "auctions/index.html", {
        "active_listings" : active_listings
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

@login_required(login_url='login')
def create_listing(request):
    if request.method == "POST":
        item_title = request.POST["item_name"]
        description = request.POST["description"]
        cat_id = request.POST["category"]
        starting_bid = request.POST["starting_bid"]
        image_url = request.POST["image_url"]
        img1 = request.POST["image1"]
        img2 = request.POST["image2"]
        img3 = request.POST["image3"]
        img4 = request.POST["image4"]
            
        category = Category.objects.get(pk=cat_id)

        # Create new Listing
        new_listing = Listing(
            item_name = item_title,
            description = description,
            starting_bid = starting_bid,
            current_price = starting_bid,
            category = category,
            image_url = image_url,
            owner = request.user
        )
        new_listing.save()
        
        imgs = [img1, img2, img3, img4]
        for img in imgs:
            ListingImage(listing = new_listing, image_url = img).save()
        
        return HttpResponseRedirect(reverse("index"))


    category_list = Category.objects.all()
    return render(request, "auctions/create_listing.html", {
        "category_list": category_list
    })
    

def categories(request):
    pass

def listing_detail(request, item_id):
    listing = Listing.objects.get(pk=item_id)
    images = ListingImage.objects.filter(listing=listing).all()
    return render(request, "auctions/listing.html", {
        "listing": listing,
        "images": images
    })

def bid(request):
    # TODO Complete the implementation
    raise NotImplementedError