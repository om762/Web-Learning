from django.contrib.auth import authenticate, login, logout
from django.db.models import F
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponseRedirect, Http404

from django.views.decorators.http import require_POST
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse

from .models import *

# Home Page
def index(request):
    if request.user.is_authenticated:
        watchlist = request.user.watchlist.all()
        watchlist_count = watchlist.count()
    else:
        watchlist = None
        watchlist_count = 0
    active_listings = Listing.objects.filter(active=True).order_by(F('created_at').desc())
    return render(request, "auctions/index.html", {
        "active_listings": active_listings,
        "watchlist_count": watchlist_count,
        "watchlist": watchlist
    })

# All Listing Page
def all_listings(request):
    if request.user.is_authenticated:
        watchlist = request.user.watchlist.all()
        watchlist_count = watchlist.count()
    else:
        watchlist = None
        watchlist_count = 0
    all_listings = Listing.objects.all().order_by(F('created_at').desc())
    return render(request, "auctions/all_listing.html", {
        "all_listings": all_listings,
        "watchlist_count": watchlist_count,
        "watchlist": watchlist
    })

# Login Page 
def login_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse("index"))
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

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

# Registration Page 
def register(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse("index"))

    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

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

# Create New Listing Page 
@login_required(login_url='login')
def create_listing(request):
    if request.method == "POST":
        item_title = request.POST["item_name"]
        description = request.POST["description"]
        cat_id = request.POST.get("category")
        starting_bid = request.POST["starting_bid"]
        image_url = request.POST.get("image_url")
        img1 = request.POST.get("image1")
        img2 = request.POST.get("image2")
        img3 = request.POST.get("image3")
        img4 = request.POST.get("image4")

        if cat_id:
            category = Category.objects.get(pk=cat_id)
        else:
            category = Category.objects.get(type="Uncategorized")
            
        if not image_url:
            image_url = f"https://placehold.co/350x200/fff/31343C?font=lora&text={item_title}"

        new_listing = Listing(
            item_name=item_title,
            description=description,
            starting_bid=starting_bid,
            current_price=starting_bid,
            category=category,
            image_url=image_url,
            owner=request.user
        )
        new_listing.save()

        imgs = [img1, img2, img3, img4]
        for img in imgs:
            if img:
                ListingImage(listing=new_listing, image_url=img).save()

        return HttpResponseRedirect(reverse("index"))

    category_list = Category.objects.all()
    watchlist_count = request.user.watchlist.count()
    return render(request, "auctions/create_listing.html", {
        "category_list": category_list,
        "watchlist_count": watchlist_count
    })

# Categories Page
def categories(request):
    categories = Category.objects.all()
    context = {
        "categories": categories,
    }

    if request.user.is_authenticated:
        context["watchlist_count"] = request.user.watchlist.count()
    else:
        context["watchlist_count"] = 0

    return render(request, "auctions/categories.html", context)

# Item Of the Category
def category(request, type):
    category = get_object_or_404(Category, type=type)
    listings = Listing.objects.filter(category=category)
    context = {
        "category": category,
        "listings": listings,
    }

    if request.user.is_authenticated:
        watchlist = request.user.watchlist.all()
        context["watchlist"] = watchlist
        context["watchlist_count"] = watchlist.count()
    else:
        context["watchlist_count"] = 0

    return render(request, "auctions/category.html", context)

# Listing Detail Page
def listing_detail(request, item_id):
    try:
        item_id = int(item_id)
    except ValueError:
        raise Http404

    listing = get_object_or_404(Listing, pk=item_id)
    images = listing.images.all()
    comments = listing.comments.order_by('-created_at')
    top_bids = listing.bids.order_by('-amount')[:5]
    context = {
        "listing": listing,
        "images": images,
        "comments": comments,
        "top_bids": top_bids,
    }

    if request.user.is_authenticated:
        is_in_watchlist = request.user.watchlist.filter(pk=listing.pk).exists()
        watchlist_count = request.user.watchlist.count()
        context.update({
            "is_in_watchlist": is_in_watchlist,
            "watchlist_count": watchlist_count,
        })

        if request.method == "POST":
            bidding_amount = request.POST.get("bidding_amount")
            if bidding_amount is None:
                return redirect('listing_detail', item_id=item_id)

            try:
                bidding_amount = int(bidding_amount)
            except ValueError:
                context.update({
                    "message": "Invalid bid amount.",
                    "status": "error",
                })
                return render(request, "auctions/listing.html", context)

            if bidding_amount <= listing.current_price:
                context.update({
                    "message": "Bid must be higher than the current price.",
                    "status": "error",
                })
                return render(request, "auctions/listing.html", context)

            Bid.objects.create(amount=bidding_amount, listing=listing, bidder=request.user)

            listing.current_price = bidding_amount
            listing.save()

            context.update({
                "message": "Your bid was successfully placed.",
                "status": "success",
            })

    else:
        context.update({
            "watchlist_count": 0,
            "is_in_watchlist": False,
        })

    return render(request, "auctions/listing.html", context)


# Comment Function
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

# Watchlist add and remove function
@login_required(login_url='login')
@require_POST
def add_to_watchlist(request):
    listing_id = request.POST.get("listing_id")
    listing = Listing.objects.get(pk=listing_id)

    if request.user.watchlist.filter(pk=listing.pk).exists():
        request.user.watchlist.remove(listing)
    else:
        request.user.watchlist.add(listing)

    referer = request.META.get('HTTP_REFERER', '/')
    return redirect(referer)

# Watchlist View Page
@login_required(login_url='login')
def watchlist_view(request):
    listings = request.user.watchlist.all()
    watchlist_count = listings.count()

    return render(request, "auctions/watchlist.html", {
        "listings": listings,
        "watchlist_count": watchlist_count,
        "watchlist": listings
    })

# Close Bidding Functions 
@login_required(login_url='login')
def close_bidding(request):
    if request.method == "POST":
        listing_id = request.POST.get("listing_id")
        listing = get_object_or_404(Listing, pk=listing_id)

        if request.user == listing.owner:
            listing.active = False
            listing.save()

            top_bid = Bid.objects.filter(listing=listing).order_by('-amount').first()
            if top_bid:
                listing.winner = top_bid.bidder
                listing.current_price = top_bid.amount
                listing.save()

        return redirect('listing_detail', item_id=listing_id)

# Profile Page 
@login_required(login_url='login')
def profile_view(request):
    user = request.user
    watchlist = user.watchlist.all()
    listings = Listing.objects.filter(owner=user)
    won_listings = user.won_listings.all()
    return render(request, 'auctions/profile.html', {
        'user': user,
        'watchlist': watchlist,
        "watchlist_count": watchlist.count(),
        'listings': listings,
        'won_listings': won_listings
    })

# Page Not Found
def page_not_found(request, invalid_path):
    return render(request, '404.html', status=404)