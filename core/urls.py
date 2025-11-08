from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from . import views

urlpatterns = [
    # ============ Аутентификация ============
    path('auth/register/', views.register, name='api_register'),
    path('auth/login/', views.login, name='api_login'),

    # ✅ Используем стандартный view из SimpleJWT (а не views.token_refresh)
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # ============ Пользователи ============
    path('users/profile/', views.UserProfileView.as_view(), name='user_profile'),
    path('users/', views.UserListView.as_view(), name='user_list'),

    # ============ Авторы ============
    path('authors/', views.AuthorListView.as_view(), name='author_list'),
    path('authors/<int:pk>/', views.AuthorDetailView.as_view(), name='author_detail'),

    # ============ Книги ============
    path('books/', views.BookListView.as_view(), name='book_list'),
    path('books/<int:pk>/', views.BookDetailView.as_view(), name='book_detail'),

    # ============ Займы ============
    path('loans/', views.BookLoanListView.as_view(), name='loan_list'),
    path('loans/<int:pk>/', views.BookLoanDetailView.as_view(), name='loan_detail'),
]
