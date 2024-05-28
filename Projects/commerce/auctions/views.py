from django.contrib.auth import authenticate, login, logout
from django.db.models import F
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse

from .models import *


def index(request):
        if request.user.is_authenticated:
            watchlist_count = Watchlist.objects.filter(user=request.user).count()
        else:
            watchlist_count = 0
        active_listings = Listing.objects.filter(active=True).order_by(F('created_at').desc())
        return render(request, "auctions/index.html", {
        "active_listings" : active_listings,
        "watchlist_count":watchlist_count
    })


def login_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse("index")) # Redirecting to profile will be better
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
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse("index")) # Redirecting to profile will be better

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
    watchlist_count = Watchlist.objects.filter(user=request.user).count()
    return render(request, "auctions/create_listing.html", {
        "category_list": category_list,
        "watchlist_count": watchlist_count
    })
    

def categories(request):
    categories = Category.objects.all()
    return render(request, "auctions/categories.html", {
        "categories": categories
    })

def category(request, type):
    categories = Category.objects.all()
    category = Category.objects.filter(type=type).first()
    
    if category:
        listings = Listing.objects.filter(category=category)
        return render(request, "auctions/category.html", {
            "listings": listings,
            "category": category
        })
    
    if request.user.is_authenticated:
        watchlist_count = Watchlist.objects.filter(user=request.user).count()
    else:
        watchlist_count = 0
    return render(request, "auctions/categories.html", {
        "categories": categories,
        "watchlist_count":watchlist_count
    })


def listing_detail(request, item_id):
    listing = Listing.objects.get(pk=item_id)
    images = ListingImage.objects.filter(listing=listing).all()
    comments = Comment.objects.filter(listing=listing).order_by(F('created_at').desc())
    is_in_watchlist = False
    if request.user.is_authenticated:
        is_in_watchlist = Watchlist.objects.filter(user=request.user, listing=listing).exists()
        watchlist_count = Watchlist.objects.filter(user=request.user).count()
    else:
        watchlist_count = 0
    return render(request, "auctions/listing.html", {
        "listing": listing,
        "images": images,
        "comments":comments,
        "is_in_watchlist": is_in_watchlist,
        "watchlist_count": watchlist_count
    })

@login_required(login_url='login')
def bid(request):
    if request.method == "POST":
        bidding_amount = request.POST.get("bidding_amount")
        listing_id = request.POST.get("listing_id")
        listing = Listing.objects.get(pk=listing_id)
        images = ListingImage.objects.filter(listing=listing).all()
        comments = Comment.objects.filter(listing=listing).order_by(F('created_at').desc())
        watchlist_count = Watchlist.objects.filter(user=request.user).count()

        try:
            bidding_amount = int(bidding_amount)
        except ValueError:
            return render(request, "auctions/listing.html", {
                "bidding_amount": bidding_amount,
                "message": "Invalid bid amount.",
                "status" :  "error",
                "listing": listing,
                "images": images,
                "comments": comments,
                "watchlist_count": watchlist_count
            })

        if bidding_amount <= listing.current_price:
            return render(request, "auctions/listing.html", {
                "bidding_amount": bidding_amount,
                "message": "Bid must be higher than the current price.",
                "status" : "error",
                "listing": listing,
                "images": images,
                "comments":comments,
                "watchlist_count": watchlist_count
            })

        new_bid = Bid(amount=bidding_amount, listing=listing, bidder=request.user)
        new_bid.save()

        # Update the current price of the listing
        listing.current_price = bidding_amount
        listing.save()
        
        watchlist_count = Watchlist.objects.filter(user=request.user).count()
        return render(request, "auctions/listing.html", {
                        "message": "Your bid was successfully placed.",
                        "status" : "success",
                        "listing": listing,
                        "images": images,
                        "comments": comments,
                        "watchlist_count":watchlist_count
                    })

@login_required(login_url='login')
def add_comment(request):
    if request.method == "POST":
        text = request.POST.get("comment_text")
        listing_id = request.POST.get("listing_id")
        listing = Listing.objects.get(pk=listing_id)
        commenter = request.user
        new_comment = Comment(text=text, listing=listing, commenter=commenter)
        new_comment.save()
        return redirect(f'/listing/{listing_id}#comment')

@login_required(login_url='login')
def watchlist(request):
    if request.method == "POST":
        listing_id = request.POST.get("listing_id")
        listing = Listing.objects.get(pk=listing_id)
        
        if Watchlist.objects.filter(user=request.user, listing=listing).exists():
            Watchlist.objects.get(user=request.user, listing=listing).delete()
            return redirect(f"/listing/{listing_id}")
        
        Watchlist(user=request.user, listing=listing).save()
        return redirect(f"/listing/{listing_id}")

    watchlist = Watchlist.objects.filter(user=request.user)
    listings = [item.listing for item in watchlist]
    
    watchlist_count = len(listings)
    
    return render(request, "auctions/watchlist.html", {
        "listings": listings,
        "watchlist_count": watchlist_count
    })
