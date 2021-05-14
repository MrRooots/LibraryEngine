from django.db import models
from django.utils.text import slugify
from time import time
from django.shortcuts import reverse


# Function that build slug from the book title
def build_slug(title):
  return '{}-{}'.format(slugify(title, allow_unicode=True), str(int(time())))


# Book model
class Book(models.Model):
  title = models.TextField(max_length=150, db_index=True)  # Book title
  slug = models.SlugField(max_length=50, unique=True)  # Book url
  content = models.TextField(db_index=True)  # Book description
  publish_date = models.DateTimeField(auto_now_add=True)  # Date of page creation
  tags = models.ManyToManyField('Tag', related_name='books', blank=True)  # Tag relations
  objects = models.Manager()  # Quick 'fix' for vscode pylint

  # Overloaded object.save() method, that support auto slug gen and the title will be uppercased
  def save(self, *args, **kwargs):
    self.title = self.title.title()
    if not self.slug:
      self.slug = build_slug(self.title)

    super().save(*args, **kwargs)

  def get_absolute_url(self):
    return reverse('display_book_url', kwargs={'slug': self.slug})

  def get_update_url(self):
    return reverse('book_update_url', kwargs={'slug': self.slug})

  def get_delete_url(self):
    return reverse('book_delete_url', kwargs={'slug': self.slug})

  def __str__(self):
    return self.title


# Tag model
class Tag(models.Model):
  title = models.CharField(max_length=50, unique=True, db_index=True)  # Tag title
  slug = models.SlugField(max_length=50, unique=True)  # Tag url
  objects = models.Manager()  # Quick 'fix' for vscode pylint

  # Overloaded object.save() method, that support auto slug gen and the title will be uppercased
  def save(self, *args, **kwargs):
    self.title = self.title.title()
    if not self.slug:
      self.slug = slugify(self.title) + '-tag'

    super().save(*args, **kwargs)

  def get_update_url(self):
    return reverse('tag_update_url', kwargs={'slug': self.slug})

  def get_delete_url(self):
    return reverse('tag_delete_url', kwargs={'slug': self.slug})

  def get_absolute_url(self):
    return reverse('associated_books_url', kwargs={'slug': self.slug})

  def __str__(self):
    return self.title

    # 11.45->12.45..13.45..14.45..15.20->16.10
