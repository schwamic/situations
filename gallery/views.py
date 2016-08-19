from django.shortcuts import render
from django.views import generic
from .models import Publisher, Image, Post

class Posts(generic.ListView):
    model = Post
    template_name = 'gallery/posts.html'