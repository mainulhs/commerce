from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse
import datetime
from django.shortcuts import get_object_or_404

from .models import User, Listing, Category, Bid, Comment, Watchlist, Winner


def index(request):
    listings = Listing.objects.all()
    user = request.user
    watchlist_count = 0  # Default value for unauthenticated users

    if user.is_authenticated:
        watchlist_count = Watchlist.objects.filter(watcher=user).count()
    
    context = {
        "listings": listings,
        "watchlist_count": watchlist_count,
    }


    return render(request, "auctions/index.html", context)

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
    
def create_listing(request):
    if request.method == "POST":
        title = request.POST["title"]
        description = request.POST["description"]
        starting_bid = request.POST["starting_bid"]
        image_url = request.FILES["image_url"]
        category = Category.objects.get(category=request.POST["category"])
        is_active = request.POST["is_active"]
        created_by = User.objects.get(username=request.user.username)
        created_on = request.POST["created_on"]

        # Attempt to create new listing
        try:
            listing = Listing.objects.create(title=title, description=description, starting_bid=starting_bid, image_url=image_url, category=category, is_active=is_active, created_by=created_by, created_on=created_on)
            listing.save()
        except IntegrityError:
            return render(request, "auctions/create_listing.html", {
                "message": "Listing already exists."
            })
        return HttpResponseRedirect(reverse("index"))
    else:
        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse("login"))
        else:
            if request.user.is_authenticated:
              watchlist_count = Watchlist.objects.filter(watcher=request.user).count() 
            
            return render(request, "auctions/create_listing.html", {
            "date": datetime.datetime.now(),
            "categories": Category.objects.all(),
            "watchlist_count": watchlist_count,
        })

def listing(request, listing_id):
    listing = get_object_or_404(Listing, pk=listing_id)
    bids = Bid.objects.filter(listing=listing)
    # From bid show the highest bid
    if bids:
        # current bit is the last bid in the list
        current_bid = bids.last().bid
        highest_bid = Bid.objects.filter(listing=listing).order_by('-bid')[0].bid
        highest_bidder = Bid.objects.filter(listing=listing).order_by('-bid')[0].bidder
        total_bids = Bid.objects.filter(listing=listing).count()
    else:
        current_bid = 0
        highest_bid = 0
        highest_bidder = "No bidder yet."
        total_bids = 0
    comments = Comment.objects.filter(listing=listing)
    
    is_in_watchlist = False
    watchlist_count = 0  # Default value for unauthenticated users

    if request.user.is_authenticated:
        is_in_watchlist = Watchlist.objects.filter(listing=listing, watcher=request.user).exists()
        watchlist_count = Watchlist.objects.filter(watcher=request.user).count()

    # Check if the user is the winner of this listing
    winning_message = None
    winning_username = None
    winner = Winner.objects.filter(listing=listing)
    if winner.exists():
        winning_message = "Congratulations! You won this listing."
        winning_username = winner[0].winner.username
        
    if request.method == "POST":
        bid = request.POST["bid"]
        
        if bid == "":
            return render(request, "auctions/listing.html", {
                "listing": listing,
                "bids": bids,
                "comments": comments,
                "is_in_watchlist": is_in_watchlist,
                "message": "Bid must be greater than 0."
            })
        elif float(bid) <= listing.starting_bid:
            return render(request, "auctions/listing.html", {
                "listing": listing,
                "bids": bids,
                "comments": comments,
                "is_in_watchlist": is_in_watchlist,
                "message": "Bid must be greater than the starting bid."
            })
        else:
            Bid.objects.create(listing=listing, bidder=request.user, bid=bid)
            return HttpResponseRedirect(reverse("listing", args=(listing.id,)))
        
    context = {
        "listing": listing,
        "bids": bids,
        "current_bid": current_bid,
        "highest_bid": highest_bid,
        "highest_bidder": highest_bidder,
        "total_bids": total_bids,
        "comments": comments,
        "is_in_watchlist": is_in_watchlist,
        "watchlist_count": watchlist_count,
        "winning_message": winning_message,
        "winning_username": winning_username,
    }

    return render(request, "auctions/listing.html", context)
    
def delete_listing(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)
    # get the created_by user based on the listing_id and compare to the current user to see if they match then delete the listing if they don't match return an error message
    if listing.created_by == request.user:
        listing.delete()
        return HttpResponseRedirect(reverse("index"))
    else:
        if request.user.is_authenticated:
            watchlist_count = Watchlist.objects.filter(watcher=request.user).count()
        return render(request, "auctions/index.html", {
            "watchlist_count": watchlist_count,
            "message": "You are not authorized to delete this listing."
        })
    
def add_to_watchlist(request, listing_id):
    listing = get_object_or_404(Listing, pk=listing_id)
    Watchlist.objects.create(listing=listing, watcher=request.user)
    return redirect('listing', listing_id=listing_id)

def remove_from_watchlist(request, listing_id):
    listing = get_object_or_404(Listing, pk=listing_id)
    Watchlist.objects.filter(listing=listing, watcher=request.user).delete()
    return redirect('listing', listing_id=listing_id)

def watchlist(request):
    if request.user.is_authenticated:
        watchlist_items = Watchlist.objects.filter(watcher=request.user)
        watchlist_count = Watchlist.objects.filter(watcher=request.user).count()
        context = {
            "watchlist_items": watchlist_items,
            "watchlist_count": watchlist_count,
        }
        return render(request, "auctions/watchlist.html", context)
    else:
        # Redirect the user to the login page or another appropriate page for anonymous users
        return HttpResponseRedirect(reverse("login"))


def add_bid(request, listing_id):
    listing = get_object_or_404(Listing, pk=listing_id)
    bid = request.POST["bid"]
    Bid.objects.create(listing=listing, bidder=request.user, bid=bid)
    return redirect('listing', listing_id=listing_id)

def add_comment(request, listing_id):
    listing = get_object_or_404(Listing, pk=listing_id)
    comment = request.POST["comment"]
    Comment.objects.create(listing=listing, commenter=request.user, comment=comment)
    return redirect('listing', listing_id=listing_id)

def close_listing(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)
    winner = Winner.objects.filter(listing=listing)

    watchlist_count = 0  # Default value for unauthenticated users
    if request.user.is_authenticated:
        watchlist_count = Watchlist.objects.filter(watcher=request.user).count()

    if winner.exists():
        return render(request, "auctions/listing.html", {
            "listing": listing,
            "watchlist_count": watchlist_count,
            "message": "This listing is already closed."
        })
    
    # Check if the user can close the listing
    if listing.created_by == request.user:
        # Get the highest bid
        highest_bid = Bid.objects.filter(listing=listing).order_by('-bid')[0]
        # Create a winner record
        Winner.objects.create(listing=listing, winner=highest_bid.bidder)
        # Close the listing
        listing.is_active = False
        listing.save()
        return redirect('listing', listing_id=listing_id)
    else:
        if request.user.is_authenticated:
            watchlist_count = Watchlist.objects.filter(watcher=request.user).count()
        return render(request, "auctions/index.html", {
            "watchlist_count": watchlist_count,
            "message": "You are not authorized to close this listing."
        })
    

    