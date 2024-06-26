from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create_listing", views.create_listing, name="create_listing"),
    path("listing/<int:listing_id>", views.listing, name="listing"),
    path("edit_listing/<int:listing_id>", views.edit_listing, name="edit_listing"),
    path("delete_listing/<int:listing_id>", views.delete_listing, name="delete_listing"),
    path("close_listing/<int:listing_id>", views.close_listing, name="close_listing"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("add_to_watchlist/<int:listing_id>", views.add_to_watchlist, name="add_to_watchlist"),
    path("remove_from_watchlist/<int:listing_id>", views.remove_from_watchlist, name="remove_from_watchlist"),
    path("add_bid/<int:listing_id>", views.add_bid, name="add_bid"),
    path("add_comment/<int:listing_id>", views.add_comment, name="add_comment"),
    path("categories", views.categories, name="categories"),
    path("category/<str:category>", views.category, name="category"),
]
