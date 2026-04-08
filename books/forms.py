from django import forms
from .models import Book


class BookForm(forms.ModelForm):
    """Form for creating and updating books"""

    class Meta:
        model = Book
        fields = [
            'title',
            'author',
            'genre',
            'publication_year',
            'isbn',
            'description',
            'is_available'
        ]

        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter book title'
            }),
            'author': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter author name'
            }),
            'genre': forms.Select(attrs={
                'class': 'form-control'
            }),
            'publication_year': forms.NumberInput(attrs={
                'class': 'form-control'
            }),
            'isbn': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4
            }),
            'is_available': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }

    def clean_title(self):
        title = self.cleaned_data.get('title')
        if len(title) < 2:
            raise forms.ValidationError("Title must be at least 2 characters long")
        return title