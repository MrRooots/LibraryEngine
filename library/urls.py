from django.urls import path
from .views import display_books, display_tags
from .views import BookDetail, BookCreate, BookDelete, BookUpdate
from .views import TagDetail, TagCreate, TagDelete, TagUpdate

urlpatterns = [
  path('', display_books, name='display_catalog_url'),

  path('book/create/', BookCreate.as_view(), name='book_create_url'),
  path('book/delete/<str:slug>/', BookDelete.as_view(), name='book_delete_url'),
  path('book/update/<str:slug>/', BookUpdate.as_view(), name='book_update_url'),
  path('book/<str:slug>/', BookDetail.as_view(), name='display_book_url'),

  path('tags/', display_tags, name='display_tags_url'),
  path('tag/create', TagCreate.as_view(), name='tag_create_url'),
  path('tag/delete/<str:slug>', TagDelete.as_view(), name='tag_delete_url'),
  path('tag/update/<str:slug>', TagUpdate.as_view(), name='tag_update_url'),
  path('tag/<str:slug>', TagDetail.as_view(), name='associated_books_url'),
]
