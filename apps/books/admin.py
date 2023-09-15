from django.contrib import admin
from .models import Book, Borrowing, ReservedItem, WishlistItem


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'edition', 'author', 'publisher', 'genre', 'isbn', 'first_pub', 'last_pub', 'language', 'no_of_books', 'is_available', )
    list_filter = ("title", "author", "publisher",)
    search_fields = ("title", "author", "publisher",)
    list_per_page = 20

@admin.register(Borrowing)
class BorrowingAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'book', 'borrow_date', 'due_date', 'return_date', 'fine', )
    list_filter = ("user", "book", "borrow_date",)
    search_fields = ("user", "book", "borrow_date",)
    list_per_page = 20
    
@admin.register(ReservedItem)
class ReservedItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'book', 'reserved_date', 'available_notification_sent', )
    list_filter = ("user", "book", "reserved_date", "available_notification_sent", )
    search_fields = ("user", "book", "reserved_date", "available_notification_sent", )
    list_per_page = 20
    
@admin.register(WishlistItem)
class WishlistItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'book', 'added_date', )
    list_filter = ("user", "book", "added_date",)
    search_fields = ("user", "book", "added_date",)
    list_per_page = 20
