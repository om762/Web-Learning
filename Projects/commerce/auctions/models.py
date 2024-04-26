from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    id = models.BigAutoField(primary_key=True)


class Listing(models.Model):
    id = models.BigAutoField(primary_key=True)
    item_name = models.CharField(max_length=100)
    description = models.CharField(max_length=5000)
    starting_bid = models.IntegerField()
    category = models.ForeignKey('Category', on_delete=models.CASCADE, related_name="items")
    active = models.BooleanField(default=True)
    image_url = models.URLField(blank=True)
    
    def __str__(self) -> str:
        return self.item_name

class Category(models.Model):
    id = models.BigAutoField(primary_key=True)
    type = models.CharField(max_length=35)

    def __str__(self) -> str:
        return self.type