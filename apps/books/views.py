from rest_framework import viewsets, status
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from datetime import datetime, timedelta
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.core.mail import send_mail
from .serializers import BookSerializer, BorrowingSerializer,ReservedItemSerializer, WishlistItemSerializer
from .models import Book, Borrowing, ReservedItem, WishlistItem


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    
    filter_backends = [DjangoFilterBackend]  
    filterset_fields = {
        "title": ["exact", "icontains"],  
        "author": ["exact", "icontains"],  
        "publisher": ["exact", "icontains"],  
    }
    
    
class BorrowingViewSet(viewsets.ModelViewSet):
    queryset = Borrowing.objects.all()
    serializer_class = BorrowingSerializer
    
    def create(self, request, *args, **kwargs):
        book_id = request.data.get('book')
        book = Book.objects.get(id=book_id)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.request.user
        if book.is_available:  
            borrowing = Borrowing(user=user, book=book)
            borrowing.borrow_date = datetime.now()
            due_date_str = request.data['due_date']
            borrowing.due_date = datetime.strptime(due_date_str, '%Y-%m-%d')  
            borrowing.save()
            book.no_of_books -= 1
            if book.no_of_books<1:
                book.is_available = False
            book.save()
            return Response({'message': 'Book borrowed successfully.', 'borrowing_details': serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'Book is not available for borrowing.'}, status=status.HTTP_204_NO_CONTENT)
        

    @action(detail=True, methods=['post'])
    def return_book(self, request, pk=None):
        borrowing = self.get_object()
        book = borrowing.book
        if borrowing.user != request.user:
            return Response({'message': 'You are not authorized to return this book.'}, status=status.HTTP_401_UNAUTHORIZED)
        if not borrowing.return_date:
            borrowing.return_date = timezone.now()
            book.is_available = True
            book.no_of_books += 1
            book.save()
            borrowing.fine = borrowing.calculate_fine()
            borrowing.save()
            
            return Response({'message': 'Book returned successfully.'}, status=status.HTTP_201_CREATED)    
        else:
            return Response({'message': 'Book has already been returned.'}, status=status.HTTP_400_BAD_REQUEST)
    

class ReservedItemViewSet(viewsets.ModelViewSet):
    serializer_class = ReservedItemSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return ReservedItem.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        user = self.request.user
        book = serializer.validated_data['book']
        existing_reserved_item = ReservedItem.objects.filter(user=user, book=book).first()
        
        if existing_reserved_item:
            return Response({'message': 'You have already reserved this book! You will be notified when the book will be available.'}, status=status.HTTP_400_BAD_REQUEST)
        
        if book.is_available:
            return Response({'message': 'Book is available! You can borrow now.'}, status=status.HTTP_400_BAD_REQUEST)
        
        if not book.is_available:
            serializer.save(user=user)
            return Response({'message': 'Book reserved successfully. You will be notified when the book will be available.', 'Details': serializer.data}, status=status.HTTP_201_CREATED)
        
        if book.is_available and not existing_reserved_item.available_notification_sent:
            subject = f'Book Available: {book.title}'
            message = f'Dear {user.username},\n\nThe book "{book.title}" you reserved is now available. You can borrow it from the library.\n\nThank you!'
            send_mail(subject, message, 'my_email@example.com', [user.email], fail_silently=False)
            existing_reserved_item.available_notification_sent = True
            existing_reserved_item.save()
            return Response({'message': 'Book is now available and you have been notified.', 'Details': serializer.data}, status=status.HTTP_200_OK)
 
        
class WishlistItemViewSet(viewsets.ModelViewSet):
    serializer_class = WishlistItemSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return WishlistItem.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        user = self.request.user
        book = serializer.validated_data['book']
        existing_wishlist_item = WishlistItem.objects.filter(user=user, book=book).first()
        
        if existing_wishlist_item:
            return Response({'message': 'This book is already in your wishlist.'}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer.save(user=user)
        return Response({'message': 'The book is added in your wishlist successfully.', 'Details': serializer.data}, status=status.HTTP_201_CREATED)

    
    
    # filterset_fields = {
    #     "created_time": ("gte", "lte", ),
    #     "updated_time": ("gte", "lte", ),
    #     "user__username": ("icontains",),
    # }
    