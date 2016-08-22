from django.views import generic
from .models import Image, Post
from itertools import chain

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

    def get_queryset(self):
        slice_pos = self.get_start_position('28a505e3-c094-4ec6-8085-cced5dcb04cb', Image.objects.count())

        #split queryset with the slice-operation
        first_list = Image.objects.all()[:slice_pos]
        second_list = Image.objects.all()[slice_pos:]

        #merge the two querysets with itertools/chain
        merge_queryset = list(chain(second_list, first_list))
        return merge_queryset

class MapView(generic.ListView):
    model = Post
    template_name = 'gallery/map.html'

class PostsView(generic.ListView):
    model = Post
    template_name = 'gallery/posts.html'
    paginate_by = 25




# note:
# a[start:end] # items start through end-1
# a[start:]    # items start through the rest of the array
# a[:end]      # items from the beginning through end-1
# a[:]         # a copy of the whole array
