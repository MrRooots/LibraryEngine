from django import forms
from django.utils.text import slugify
from django.core.exceptions import ValidationError
from .models import Book, Tag


class BookCreateForm(forms.ModelForm):
  class Meta:
    model = Book
    fields = [
      'title', 'content', 'tags'
    ]
    widgets = {
      'title': forms.TextInput(attrs={'class': 'form-control'}),
      'content': forms.Textarea(attrs={'class': 'form-control'}),
      'tags': forms.SelectMultiple(attrs={'class': 'form-control'})
    }


class TagCreateForm(forms.ModelForm):
  class Meta:
    model = Tag
    fields = [
      'title'
    ]
    widgets = {
      'title': forms.TextInput(attrs={'class': 'form-control'}),
    }

  # Function that doesn't accept existing tag
  def clean_title(self):
    slug = slugify(self.cleaned_data['title']) + '-tag'

    if Tag.objects.filter(slug__iexact=slug).count():
      raise ValidationError('The tag must be unique! We already have "{}" tag'.format(self.cleaned_data['title']))

    return self.cleaned_data['title']
