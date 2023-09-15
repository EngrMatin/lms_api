# Generated by Django 4.2.1 on 2023-09-02 11:06

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('books', '0002_alter_book_first_pub_alter_book_genre_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='genre',
            field=models.CharField(blank=True, choices=[('Mystery', 'Mystery'), ('Adventure', 'Adventure'), ('Computer Science', 'Computer Science'), ('Thriller', 'Thriller'), ('Humor', 'Humor'), ('Poetry', 'Poetry'), ('Autobiography', 'Autobiography'), ('Drama', 'Drama'), ('Sci-Fiction', 'Sci-Fiction'), ('Comedy', 'Comedy'), ('Horror', 'Horror'), ('Religious', 'Religious'), ('Novel', 'Novel')], max_length=64, null=True),
        ),
        migrations.CreateModel(
            name='ReservedItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.TextField()),
                ('reserved_date', models.DateTimeField(auto_now_add=True)),
                ('is_read', models.BooleanField(default=False)),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='books.book')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
