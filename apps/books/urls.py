from django.urls import path, include
from rest_framework import routers
from .views import BookViewSet, BorrowingViewSet, ReservedItemViewSet, WishlistItemViewSet

app_name = "books"
router = routers.DefaultRouter()
router.register(r"books", BookViewSet, basename="books")
router.register(r"borrowings", BorrowingViewSet, basename="borrowings")
router.register(r"reservelist", ReservedItemViewSet, basename="reservelist")
router.register(r"wishlist", WishlistItemViewSet, basename="wishlist")

urlpatterns = [
    path("", include(router.urls)),
]
