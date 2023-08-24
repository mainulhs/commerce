from django.contrib import admin

# Register your models here.

from .models import Listing, Category, User, Bid, Comment, Watchlist, Winner

admin.site.register(User)
admin.site.register(Bid)
admin.site.register(Comment)
admin.site.register(Watchlist)
admin.site.register(Listing)
admin.site.register(Category)
admin.site.register(Winner)