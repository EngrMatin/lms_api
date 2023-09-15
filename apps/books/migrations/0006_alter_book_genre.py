# Generated by Django 4.2.1 on 2023-09-15 09:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0005_remove_book_reservation_notification_sent_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='genre',
            field=models.CharField(blank=True, choices=[('Mystery', 'Mystery'), ('Poetry', 'Poetry'), ('Adventure', 'Adventure'), ('Computer Science', 'Computer Science'), ('Thriller', 'Thriller'), ('Comedy', 'Comedy'), ('Drama', 'Drama'), ('Horror', 'Horror'), ('Sci-Fiction', 'Sci-Fiction'), ('Religious', 'Religious'), ('Novel', 'Novel'), ('Humor', 'Humor'), ('Autobiography', 'Autobiography')], max_length=64, null=True),
        ),
    ]
