from django.http import HttpResponse
from django.shortcuts import redirect

def redirect_to_catalog(request):
  return redirect('display_catalog_url', permanent=True)