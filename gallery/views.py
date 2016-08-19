from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic

from .models import Image

# Create your views here.
class imageView(generic.ListView):
    model = Image
    template_name = 'gallery/images.html'