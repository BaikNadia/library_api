from django.urls import path
from . import views

urlpatterns = [
    path('', views.catalog_page, name='home'),
    path('register/', views.register_page, name='register'),
    path('login/', views.login_page, name='login'),
    path('catalog/', views.catalog_page, name='catalog'),
    path('blog/', views.blog_page, name='blog'),
]
