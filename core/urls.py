from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView
from . import views

urlpatterns = [
    # Authentication
    path('auth/register/', views.register, name='register'),
    path('auth/login/', views.login, name='login'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Users
    path('users/profile/', views.UserProfileView.as_view(), name='user-profile'),
    path('users/', views.UserListView.as_view(), name='user-list'),

    # Authors
    path('authors/', views.AuthorListView.as_view(), name='author-list'),
    path('authors/<int:pk>/', views.AuthorDetailView.as_view(), name='author-detail'),

    # Books
    path('books/', views.BookListView.as_view(), name='book-list'),
    path('books/<int:pk>/', views.BookDetailView.as_view(), name='book-detail'),

    # Book Loans
    path('loans/', views.BookLoanListView.as_view(), name='loan-list'),
    path('loans/<int:pk>/', views.BookLoanDetailView.as_view(), name='loan-detail'),
]
