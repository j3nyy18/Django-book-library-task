from django.urls import path

from .views import (
    BookListView,
    BookDetailView,
    BookCreateView,
    BookUpdateView,
    BookDeleteView,
    BorrowedBooksView,
    export_books_csv
)

urlpatterns = [
    path('books/', BookListView.as_view(), name='book_list'),
    path('books/create/', BookCreateView.as_view(), name='book_create'),
    path('books/borrowed/', BorrowedBooksView.as_view(), name='borrowed_books'),  
    path('books/<int:pk>/', BookDetailView.as_view(), name='book_detail'),
    path('books/<int:pk>/update/', BookUpdateView.as_view(), name='book_update'),
    path('books/<int:pk>/delete/', BookDeleteView.as_view(), name='book_delete'),
    path('books/export/', export_books_csv, name='export_books'),
]