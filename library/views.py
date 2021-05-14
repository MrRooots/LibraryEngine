from django.shortcuts import render
from django.views.generic import View
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import TagCreateForm, BookCreateForm
from .models import Book, Tag
from .mixins import ObjectDetailMixin, ObjectCreateMixin, ObjectDeleteMixin, ObjectUpdateMixin


# Function that will display list of books
def display_books(request):
  search_query = request.GET.get('key_word', '')

  if search_query:
    return render(request, 'library/books_list.html', context={
      'books': Book.objects.filter(Q(title__icontains=search_query) | Q(content__icontains=search_query)),
      'tags': Tag.objects.all()
    })
  else:
    return render(request, 'library/books_list.html', context={'books': Book.objects.all(), 'tags': Tag.objects.all()})


# Not optimized!!! Sorting at each request!!!
def display_tags(request):
  return render(request, 'library/tags_list.html',
                context={'tags': sorted(Tag.objects.all(), key=lambda tag: tag.title)})


""" Book section """


class BookDetail(ObjectDetailMixin, View):
  model = Book
  template = 'library/book_detail.html'


class BookCreate(LoginRequiredMixin, ObjectCreateMixin, View):
  form = BookCreateForm
  template = 'library/book_create.html'
  raise_exception = True


class BookDelete(LoginRequiredMixin, ObjectDeleteMixin, View):
  model = Book
  template = 'library/book_delete.html'
  raise_exception = True


class BookUpdate(LoginRequiredMixin, ObjectUpdateMixin, View):
  model = Book
  form_model = BookCreateForm
  template = 'library/book_update.html'
  raise_exception = True


""" Tag section """


class TagDetail(ObjectDetailMixin, View):
  model = Tag
  template = 'library/tag_detail.html'


class TagCreate(LoginRequiredMixin, ObjectCreateMixin, View):
  form = TagCreateForm
  template = 'library/tag_create.html'
  raise_exception = True


class TagDelete(LoginRequiredMixin, ObjectDeleteMixin, View):
  model = Tag
  template = 'library/tag_delete.html'
  raise_exception = True


class TagUpdate(LoginRequiredMixin, ObjectUpdateMixin, View):
  model = Tag
  form_model = TagCreateForm
  template = 'library/tag_update.html'
  raise_exception = True


""" Search Section """


def display_found(request, key_word):
  return render(request, 'library/display_found', context={
    'books': set(Book.objects.filter(content__icontains=key_word) + Book.objects.filter(title_icontains=key_word)),
    'key_word': key_word})
