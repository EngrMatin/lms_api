from rest_framework.serializers import ModelSerializer
from .models import Book, Borrowing, ReservedItem, WishlistItem


class BookSerializer(ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'


class BorrowingSerializer(ModelSerializer):
    class Meta:
        model = Borrowing
        fields = '__all__'
        

class ReservedItemSerializer(ModelSerializer):
    class Meta:
        model = ReservedItem
        fields = '__all__'

    
class WishlistItemSerializer(ModelSerializer):
    class Meta:
        model = WishlistItem
        fields = '__all__'