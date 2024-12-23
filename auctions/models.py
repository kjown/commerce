from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Category(models.Model):
    name = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.name
    
class Bid(models.Model):
    bid = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="userBid")

class Listing(models.Model):
    title = models.CharField(max_length=32)
    description = models.TextField()
    imageUrl = models.URLField(blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name="category")
    starting_price = models.ForeignKey(Bid, on_delete=models.CASCADE, blank=True, null=True,  related_name="bidPrice")
    current_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="user")
    created_time = models.DateTimeField(auto_now_add=True)
    isActive = models.BooleanField(default=True)
    watchlist = models.ManyToManyField(User, blank=True, null=True, related_name="listingWatchlist")

    def __str__(self):
        return self.title

class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="userComment")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, blank=True, null=True, related_name="listingComment")
    comment = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.author} comment on {self.listing}"

