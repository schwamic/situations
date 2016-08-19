from django.shortcuts import render
from django.views import generic
from .models import Publisher, Image, Post

class PostsView(generic.ListView):
    model = Post
    template_name = 'gallery/posts.html'
    paginate_by = 25