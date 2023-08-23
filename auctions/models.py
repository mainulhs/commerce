from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Listing(models.Model):

    title = models.CharField(max_length=64)
    description = models.TextField()
    starting_bid = models.DecimalField(max_digits=10, decimal_places=2)
    image_url = models.ImageField(null=True, blank=True, upload_to="images/")
    category = models.ForeignKey('Category', on_delete=models.CASCADE, related_name="listings")
    is_active = models.BooleanField(default=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listings")
    created_on = models.DateTimeField(auto_now_add=True)

class Category(models.Model):
    category = models.CharField(max_length=64)
    
    def __str__(self):
        return f"{self.category}"  

class Bid(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="bids")
    bidder = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bids")
    bid = models.DecimalField(max_digits=10, decimal_places=2)
    created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.listing.title} - {self.bidder} - {self.bid}"
    
class Comment(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="comments")
    commenter = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    comment = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.listing.title} - {self.commenter} - {self.comment}"

class Watchlist(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="watchlists")
    watcher = models.ForeignKey(User, on_delete=models.CASCADE, related_name="watchlists")
    created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.listing.title} - {self.watcher}"
    
class Winner(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="winners")
    winner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="winners")
    created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.listing.title} - {self.winner}"


'''
    def create_categories(apps, schema_editor):
        Category = apps.get_model("auctions", "Category")
        Category.objects.create(category="Fashion")
        Category.objects.create(category="Toys")
        Category.objects.create(category="Electronics")
        Category.objects.create(category="Home")
        Category.objects.create(category="Other")
        
'''