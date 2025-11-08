from django.contrib import admin
from .models import User, Author, Book, BookLoan


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'user_type', 'is_staff')
    list_filter = ('user_type', 'is_staff')
    search_fields = ('username', 'email')


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('name', 'birth_date')
    search_fields = ('name',)


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'isbn', 'genre', 'available_copies')
    list_filter = ('genre',)
    search_fields = ('title', 'isbn')
    filter_horizontal = ('authors',)


@admin.register(BookLoan)
class BookLoanAdmin(admin.ModelAdmin):
    list_display = ('book', 'user', 'borrowed_date', 'due_date', 'status')
    list_filter = ('status',)
    search_fields = ('book__title', 'user__username')
