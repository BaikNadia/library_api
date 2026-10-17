from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.utils import timezone


class User(AbstractUser):
    USER_TYPE_CHOICES = (
        ('reader', 'Reader'),
        ('librarian', 'Librarian'),
        ('admin', 'Admin'),
    )

    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES, default='reader')
    phone = models.CharField(max_length=15, blank=True)
    address = models.TextField(blank=True)

    def __str__(self):
        return f"{self.username} ({self.get_user_type_display()})"


class Author(models.Model):
    objects = None
    name = models.CharField(max_length=100)
    bio = models.TextField(blank=True)
    birth_date = models.DateField(null=True, blank=True)
    death_date = models.DateField(null=True, blank=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Book(models.Model):
    GENRE_CHOICES = (
        ('fiction', 'Fiction'),
        ('non-fiction', 'Non-Fiction'),
        ('science', 'Science'),
        ('technology', 'Technology'),
        ('history', 'History'),
        ('biography', 'Biography'),
        ('fantasy', 'Fantasy'),
        ('mystery', 'Mystery'),
        ('romance', 'Romance'),
        ('other', 'Other'),
    )

    title = models.CharField(max_length=200)
    authors = models.ManyToManyField(Author, related_name='books')
    isbn = models.CharField(max_length=13, unique=True)
    genre = models.CharField(max_length=20, choices=GENRE_CHOICES)
    publication_date = models.DateField(null=True, blank=True)
    publisher = models.CharField(max_length=100, blank=True)
    description = models.TextField(blank=True)
    total_copies = models.PositiveIntegerField(default=1)
    available_copies = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['title']

    def __str__(self):
        return self.title


class BookLoan(models.Model):
    STATUS_CHOICES = (
        ('borrowed', 'Borrowed'),
        ('returned', 'Returned'),
        ('overdue', 'Overdue'),
    )

    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='loans')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='loans')
    borrowed_date = models.DateTimeField(auto_now_add=True)
    due_date = models.DateField()
    returned_date = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='borrowed')

    class Meta:
        ordering = ['-borrowed_date']

    def __str__(self):
        return f"{self.book.title} - {self.user.username}"

    def is_overdue(self):
        """Проверяет, просрочен ли займ книги"""
        if self.status == 'returned':
            return False
        return timezone.now().date() > self.due_date

    def save(self, *args, **kwargs):
        """Автоматически обновляет статус на 'overdue' при сохранении"""
        if self.status != 'returned' and timezone.now().date() > self.due_date:
            self.status = 'overdue'
        super().save(*args, **kwargs)
