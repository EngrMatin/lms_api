from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import datetime, timedelta

User = get_user_model()

categories = {('Adventure','Adventure'), ('Autobiography','Autobiography'), ('Comedy','Comedy'), ('Drama','Drama'), ('Humor','Humor'), ('Horror','Horror'), ('Mystery','Mystery'), ('Novel','Novel'), ('Sci-Fiction','Sci-Fiction'), ('Computer Science','Computer Science'), ('Religious','Religious'), ('Poetry','Poetry'), ('Thriller','Thriller') }

class Book(models.Model):
    title = models.CharField(max_length=128)
    edition = models.CharField(max_length=64, default='First')
    author = models.CharField(max_length=255)
    publisher = models.CharField(max_length=255, blank=True, null=True)
    genre = models.CharField(max_length=64, choices=categories, blank=True, null=True)
    isbn = models.CharField(max_length=64, blank=True, null=True)
    first_pub = models.DateField(blank=True, null=True)
    last_pub = models.DateField(blank=True, null=True)
    language = models.CharField(max_length=100, blank=True, null=True)
    pages = models.IntegerField(blank=True, null=True)
    no_of_books = models.IntegerField(default=1)
    is_available = models.BooleanField(default=True)
    
    def __str__(self):
        return f'Title: {self.title}, Author: {self.author}'
    
    

class Borrowing(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    borrow_date = models.DateTimeField(auto_now_add=True)
    due_date = models.DateTimeField(null=True, blank=True)
    return_date = models.DateTimeField(null=True, blank=True)
    fine = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def calculate_fine(self):
        overdue_days = (timezone.now() - self.due_date).days
        daily_fine_rate = 20.00  
        max_fine_amount = 500.00  
        if overdue_days>0:
            fine = min(overdue_days * daily_fine_rate, max_fine_amount)
        else:
            fine = 0
        return fine

    def save(self, *args, **kwargs):
        if not self.due_date:
            self.due_date = self.borrow_date + timedelta(days=14)
        if not self.return_date and self.due_date < datetime.now():
            self.fine = self.calculate_fine()
        super().save(*args, **kwargs)


class ReservedItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    reserved_date = models.DateTimeField(auto_now_add=True)
    available_notification_sent = models.BooleanField(default=False)
    
    def __str__(self):
        return f'Book: {self.book}, User: {self.user}, Reserved date: {self.reserved_date}'
  
    
class WishlistItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    added_date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'Book: {self.book}, User: {self.user}, Added date: {self.added_date}'
  