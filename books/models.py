from django.db import models


class Book(models.Model):
    GENRE_CHOICES = [
        ('fiction', 'Fiction'),
        ('non_fiction', 'Non-Fiction'),
        ('science', 'Science'),
        ('history', 'History'),
        ('biography', 'Biography'),
    ]

    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    genre = models.CharField(
        max_length=20,
        choices=GENRE_CHOICES
    )
    publication_year = models.IntegerField()
    isbn = models.CharField(max_length=20)
    description = models.TextField(blank=True)
    is_available = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Book'
        verbose_name_plural = 'Books'

    def __str__(self):
        return self.title