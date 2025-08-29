from django.urls import path
from .views import create_book, get_books, get_book, update_book, delete_book

urlpatterns = [
    path('books/', get_books, name='get_books'),
    path('books/<int:book_id>/', get_book, name='get_book'),
    path('books/create/', create_book, name='create_book'),
    path('books/update/<int:book_id>/', update_book, name='update_book'),
    path('books/delete/<int:book_id>/', delete_book, name='delete_book'),
]