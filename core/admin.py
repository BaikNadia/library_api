from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Author, Book, BookLoan

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'user_type', 'is_staff')
    list_filter = ('user_type', 'is_staff', 'is_superuser')
    fieldsets = UserAdmin.fieldsets + (
        ('Additional Info', {'fields': ('user_type', 'phone', 'address')}),
    )

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('name', 'birth_date')
    search_fields = ('name',)

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'isbn', 'genre', 'total_copies', 'available_copies')
    list_filter = ('genre',)
    search_fields = ('title', 'isbn')
    filter_horizontal = ('authors',)

@admin.register(BookLoan)
class BookLoanAdmin(admin.ModelAdmin):
    list_display = ('book', 'user', 'borrowed_date', 'due_date', 'status')
    list_filter = ('status', 'borrowed_date')
    search_fields = ('book__title', 'user__username')
