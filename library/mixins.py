from django.shortcuts import render, get_object_or_404, redirect
from django.utils.text import slugify
from .models import build_slug


class ObjectDetailMixin:
  model, template = None, None

  def get(self, request, slug):
    admin_perm = True if (request.user.is_authenticated and request.user.is_staff) else False

    return render(request, self.template, context={
      self.model.__name__.lower(): get_object_or_404(self.model, slug__iexact=slug),
      'admin_perm': admin_perm  # if set to 'True' then you are able to change and delete books in 'book_detail.html'
    })


class ObjectCreateMixin:
  form, template = None, None

  def get(self, request):
    return render(request, self.template, context={'form': self.form()})

  def post(self, request):
    form = self.form(request.POST)

    if form.is_valid():
      return redirect(form.save())
    else:
      return render(request, self.template, context={'form': self.form()})


class ObjectDeleteMixin:
  model, template = None, None

  def get(self, request):
    return render(request, self.template, context={self.model.__name__.lower() + 's': self.model.objects.all()})

  def post(self, request, slug):
    self.model.objects.get(slug__iexact=slug).delete()
    if self.model.__name__.lower() == 'book':
      return redirect('display_catalog_url')
    else:
      return redirect('display_tags_url')


class ObjectUpdateMixin:
  model, form_model, template = None, None, None

  def get(self, request, slug):
    obj = self.model.objects.get(slug__iexact=slug)
    form = self.form_model(instance=obj)

    return render(request, self.template, context={'form': form, self.model.__name__.lower(): obj})

  def post(self, request, slug):
    obj = self.model.objects.get(slug__iexact=slug)
    form = self.form_model(request.POST, instance=obj)

    if form.is_valid():
      if self.model.__name__.lower() == 'tag':
        obj.slug = slugify(form.cleaned_data['title']) + '-tag'
      else:
        obj.slug = build_slug(obj.title)
      return redirect(form.save())
    else:
      return render(request, self.template, context={'form': form, self.model.__name__.lower(): obj})
