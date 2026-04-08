from django.contrib import messages
from .models import Book


class SuccessMessageMixin:
    success_message = ""

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, self.success_message)
        return response

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super().delete(request, *args, **kwargs)


class BookStatsMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        books = Book.objects.all()

        context['total_books'] = books.count()
        context['available_books'] = books.filter(is_available=True).count()
        context['borrowed_books'] = books.filter(is_available=False).count()

        return context