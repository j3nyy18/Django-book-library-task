import csv
from django.http import HttpResponse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.db.models import Q, Count
from django.urls import reverse_lazy
from django.contrib import messages

from .models import Book
from .forms import BookForm
from .mixins import SuccessMessageMixin, BookStatsMixin

class BookListView(BookStatsMixin, ListView):
    model = Book
    template_name = 'books/book_list.html'
    context_object_name = 'books'
    paginate_by = 10

    def get_queryset(self):
        queryset = Book.objects.all()

        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) |
                Q(author__icontains=search)
            )

        genre = self.request.GET.get('genre')
        if genre:
            queryset = queryset.filter(genre=genre)

        availability = self.request.GET.get('availability')
        if availability:
            if availability == 'available':
                queryset = queryset.filter(is_available=True)
            elif availability == 'borrowed':
                queryset = queryset.filter(is_available=False)

        
    
        sort = self.request.GET.get('sort')
        order = self.request.GET.get('order')

        if sort in ['title', 'author', 'publication_year']:
            if order == 'desc':
                sort = f'-{sort}'
            queryset = queryset.order_by(sort)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        books = Book.objects.all()

        context['total_books'] = books.count()
        context['available_books'] = books.filter(is_available=True).count()
        context['borrowed_books'] = books.filter(is_available=False).count()
        context['genre_stats'] = Book.objects.values('genre').annotate(count=Count('id'))
        context['recent_books'] = Book.objects.order_by('-created_at')[:5]

        return context
    
class BookDetailView(DetailView):
    model = Book
    template_name = 'books/book_detail.html'
    context_object_name = 'book'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        book = self.object

        related_books = Book.objects.filter(
            genre=book.genre
        ).exclude(id=book.id)[:5]

        context['related_books'] = related_books
        context['borrow_count'] = 0
        if not book.is_available:
            context['borrow_count'] = 1

        return context
    
class BookCreateView(SuccessMessageMixin, CreateView):
    success_message = "Book created successfully"
    model = Book
    form_class = BookForm
    template_name = 'books/book_form.html'
    success_url = reverse_lazy('book_list')

    

class BookUpdateView(SuccessMessageMixin, UpdateView):
    success_message = "Book updated successfully"
    model = Book
    form_class = BookForm
    template_name = 'books/book_form.html'

    def get_success_url(self):
        return reverse_lazy('book_detail', kwargs={'pk': self.object.pk})
    
class BookDeleteView(DeleteView):
    model = Book
    template_name = 'books/book_confirm_delete.html'
    success_url = reverse_lazy('book_list')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Book deleted successfully!')
        return super().delete(request, *args, **kwargs)
    
class BorrowedBooksView(BookStatsMixin, ListView):
    model = Book
    template_name = 'books/borrowed_books.html'
    context_object_name = 'books'
    paginate_by = 10

    def get_queryset(self):
        return Book.objects.filter(is_available=False).order_by('-updated_at')
    

def export_books_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="books.csv"'

    writer = csv.writer(response)

    writer.writerow(['Title', 'Author', 'Genre', 'Year', 'Available'])

    books = Book.objects.all()

    for book in books:
        writer.writerow([
            book.title,
            book.author,
            book.get_genre_display(),
            book.publication_year,
            'Yes' if book.is_available else 'No'
        ])

    return response