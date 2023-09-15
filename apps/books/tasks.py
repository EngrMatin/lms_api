from celery import shared_task
from django.utils import timezone
from datetime import timedelta
from django.core.mail import send_mail
from .models import Borrowing, ReservedItem, Book

@shared_task
def send_due_date_reminders():
    overdue_borrowings = Borrowing.objects.filter(due_date__lt=timezone.now(), return_date=None)
    
    for borrowing in overdue_borrowings:
        user = borrowing.user
        book = borrowing.book
        subject = f'Reminder: Return {book.title}'
        message = f'Dear {user.username},\n\nThis is a reminder to return the book "{book.title}" as it was to return at "{borrowing.due_date}".\n\nThank you!'
        send_mail(subject, message, 'engr.matin.com@gmail.com', [user.email], fail_silently=False)
 
