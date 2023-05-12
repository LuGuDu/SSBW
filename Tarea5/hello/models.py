from django.db import models
from django import forms

class FormularioLibro(forms.Form):
    title = forms.CharField(label='Title', max_length=100)
    author = forms.CharField(label='Author', max_length=100)
    genre = forms.CharField(label='Genre', max_length=100)
    description = forms.CharField(label='Description', max_length=500)
    isbn = forms.CharField(label='Isbn', max_length=100, required=False)
    publisher = forms.CharField(label='Publisher', max_length=100, required=False)
    published = forms.CharField(label='Published', max_length=25, required=False)
    """
    published = forms.DateTimeField(
        label='Published',
        required=False,
        widget=forms.DateTimeInput(
        attrs={'class': 'form-control datetimepicker-input'},
        format='%Y-%m-%d'
        )
    )
    """
