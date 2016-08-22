from django.views import generic
from .models import Publisher, Image, Post
from django.shortcuts import HttpResponse

class ImagesView(generic.ListView):
    model = Image
    template_name = 'gallery/images.html'
    paginate_by = 25

    def get_start_position(uuid, max_value):
        """
        generates a value 0 <= x < max_value using a uuid
        :return:
        """
        start_position = 0
        for letter in uuid[:9]:
            start_position += ord(letter)
        else:
            start_position *= ord(uuid[10])
            start_position %= max_value
        return start_position

    print(get_start_position('28a505e3-c094-4ec6-8085-cced5dcb04cb', Image.objects.count()))


class MapView(generic.ListView):
    model = Post
    template_name = 'gallery/map.html'

class PostsView(generic.ListView):
    model = Post
    template_name = 'gallery/posts.html'
    paginate_by = 25