from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    id = models.BigAutoField(primary_key=True)
    watchlist = models.ManyToManyField('Listing', related_name='watched_by', blank=True)


class Listing(models.Model):
    id = models.BigAutoField(primary_key=True)
    item_name = models.CharField(max_length=100)
    description = models.TextField(max_length=1000)
    starting_bid = models.IntegerField()
    current_price = models.IntegerField()
    category = models.ForeignKey('Category', blank=True, null=True, on_delete=models.SET_NULL, related_name="items")
    active = models.BooleanField(default=True)
    winner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='won_listings')
    image_url = models.URLField(blank=True)

    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owned_listings')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.item_name


class ListingImage(models.Model):
    id = models.BigAutoField(primary_key=True)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="images")
    image_url = models.URLField()

    def __str__(self) -> str:
        return f"Image for {self.listing.item_name}"


class Bid(models.Model):
    id = models.BigAutoField(primary_key=True)
    amount = models.IntegerField()
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="bids")
    bidder = models.ForeignKey(User, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"Bid of {self.amount} on {self.listing}"


class Comment(models.Model):
    id = models.BigAutoField(primary_key=True)
    text = models.CharField(max_length=1000)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="comments")
    commenter = models.ForeignKey(User, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"Comment by {self.commenter.username} on {self.listing}"


class Category(models.Model):
    id = models.BigAutoField(primary_key=True)
    type = models.CharField(max_length=35, unique=True)
    image_url = models.URLField()

    def __str__(self) -> str:
        return self.type

