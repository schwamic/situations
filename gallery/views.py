from django.views import generic
from .models import Publisher, Image, Post

class ImagesView(generic.ListView):
    model = Image
    template_name = 'gallery/images.html'

class MapView(generic.ListView):
    model = Post
    template_name = 'gallery/map.html'

class PostsView(generic.ListView):
    model = Post
    template_name = 'gallery/posts.html'
    paginate_by = 25
