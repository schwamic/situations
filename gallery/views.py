from django.views import generic
from .models import Publisher, Image, Post
from itertools import chain

class ImagesView(generic.ListView):
    model = Image
    template_name = 'gallery/images.html'
    # random_imgs_list = Image.objects.order_by('?')
    # ordering = '?'
    slice_pos = 1

    def get_queryset(self):
        #split queryset with the slice-operation
        first_list = Image.objects.all()[:self.slice_pos]
        second_list = Image.objects.all()[self.slice_pos:]

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