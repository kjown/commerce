from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib import messages

from .models import User, Category, Listing, Comment, Bid

def listing(request, id):
    listingData = Listing.objects.get(pk=id)
    isListingInWatchlist = request.user in listingData.watchlist.all()
    allComments = Comment.objects.filter(listing=listingData)
    isSeller = request.user.username == listingData.creator.username
    # watchlist_count = request.user.listingWatchlist.count()
    return render(request, "auctions/listing.html", {
        "listing": listingData,
        "isListingInWatchlist": isListingInWatchlist,
        "allComments": allComments,
        "isSeller": isSeller,
        # "watchlist_count": watchlist_count,
    })

def closeAuction(request, id):
    listingData = Listing.objects.get(pk=id)
    listingData.isActive = False
    listingData.save()
    isListingInWatchlist = request.user in listingData.watchlist.all()
    allComments = Comment.objects.filter(listing=listingData)
    isSeller = request.user.username == listingData.creator.username
    return render(request, "auctions/listing.html", {
        "listing": listingData,
        "isListingInWatchlist": isListingInWatchlist,
        "allComments": allComments,
        "isSeller": isSeller,
        "update": True,
        "message": "Congratulations! The auction is closed."
    })

def addBid(request, id):
    newBid = float(request.POST['newBid'])
    listingData = Listing.objects.get(pk=id)
    isListingInWatchlist = request.user in listingData.watchlist.all()
    allComments = Comment.objects.filter(listing=listingData)
    isSeller = request.user.username == listingData.creator.username
    if int(newBid) > listingData.starting_price.bid:
        updateBid = Bid(user=request.user, bid=newBid)
        updateBid.save()
        listingData.starting_price = updateBid
        listingData.save()
        return render(request, "auctions/listing.html", {
            "listing": listingData,
            "message": "Bid was updated sucessfully",
            "update": True,
            "isListingInWatchlist": isListingInWatchlist,
            "allComments": allComments,
            "isSeller": isSeller,
        })
    else:
        return render(request, "auctions/listing.html", {
            "listing": listingData,
            "message": "Bid failed to update. The new bid must be higher than the current bid.",
            "update": False,        
            "isListingInWatchlist": isListingInWatchlist,
            "allComments": allComments,
            "isSeller": isSeller,
        })


def addComment(request, id):
    currentUser = request.user
    listingData = Listing.objects.get(pk=id)
    comment = request.POST['newComment']
    # TODO: add time posted

    newComment = Comment(
        author=currentUser,
        listing=listingData,
        comment=comment
    )

    newComment.save()
    return HttpResponseRedirect(reverse("listing", args=(id, )))

def watchlist(request):
    currentUser = request.user
    listings = currentUser.listingWatchlist.all()
    watchlist_count = listings.count()
    return render(request, "auctions/watchlist.html", {
        "listings": listings,
        "watchlist_count": watchlist_count,
    })

def removeWatchlist(request, id):
    listingData = Listing.objects.get(pk=id)
    currentUser = request.user
    listingData.watchlist.remove(currentUser)
    return HttpResponseRedirect(reverse("listing", args=(id, )))

def addWatchlist(request, id):
    listingData = Listing.objects.get(pk=id)
    currentUser = request.user

    if not currentUser.is_authenticated:
        messages.warning(request, "You need to log in to add items to your watchlist.")
        return HttpResponseRedirect(reverse("login"))

    listingData.watchlist.add(currentUser)
    return HttpResponseRedirect(reverse("listing", args=(id, )))

def index(request):
    activeListings = Listing.objects.filter(isActive=True)
    allCategories = Category.objects.all()
    # watchlist_count = request.user.listingWatchlist.count()
    return render(request, "auctions/index.html", {
        "listings": activeListings,
        "categories": allCategories,
        # "watchlist_count": watchlist_count,
    })

def displayCategory(request, category_name):
    category = Category.objects.get(name=category_name)
    activeListings = Listing.objects.filter(isActive=True, category=category)
    allCategories = Category.objects.all()
    # watchlist_count = request.user.listingWatchlist.count()
    return render(request, "auctions/category_listing.html", {
        "listings": activeListings,
        "categories": category,
        # "watchlist_count": watchlist_count,
    })

def categories(request):
    allCategories = Category.objects.all()
    # watchlist_count = request.user.listingWatchlist.count()
    return render(request, "auctions/categories.html", {
        "categories": allCategories,
        # "watchlist_count": watchlist_count,
    })


def createListing(request):
    watchlist_count = request.user.listingWatchlist.count()

    if request.method == "GET":
        allCategories = Category.objects.all()
        return render(request, "auctions/create.html", {
            "categories": allCategories,
        })
    else:
       # Get data from the form
        title = request.POST["title"]
        description = request.POST["description"]
        imageurl = request.POST.get("imageurl", None)
        if not imageurl:
            imageurl = "https://img.freepik.com/premium-vector/default-image-icon-vector-missing-picture-page-website-design-mobile-app-no-photo-available_87543-11093.jpg?w=826"
        starting_price = request.POST["starting_price"]
        category = request.POST["category"]

        # Who is the user
        currentUser = request.user

        # Get all content about the particular category
        categoryData = Category.objects.get(name=category)

        # Create a bid object
        bid = Bid(bid=float(starting_price), user=currentUser)
        bid.save()

        # Create a new listing object
        newListing = Listing(
            title=title,
            description=description,
            imageUrl=imageurl,
            category=categoryData,
            starting_price=bid,
            creator=currentUser
        )
        # Insert the object in our database
        newListing.save()

        # Redirect to index page
        return HttpResponseRedirect(reverse(index))

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
