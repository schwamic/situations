from django.views import generic
from .models import Publisher, Image, Post
from itertools import chain

class ImagesView(generic.ListView):
    model = Image
    template_name = 'gallery/images.html'
    paginate_by = 25

    def get_uuid(self):
        """
        takes GET parm and checks correctness.
        returns a uuid if an associated user can be found.
        :return:
        """
        self.uuid = self.request.GET.get('id')

        return self.uuid

    def get_start_position(self, uuid, max_value):
        """
        generates a value 0 <= x < max_value using a uuid
        :return:
        """
        start_position = 1
        for count, letter in enumerate(uuid[:8]):  # only the first block of numbers is actually used
            if count % 2 is 0:
                start_position *= ord(letter)
            else:
                start_position += ord(letter)
        else:
            start_position %= max_value
        print(start_position)
        return start_position

    def get_queryset(self):
        slice_pos = self.get_start_position(self.get_uuid(), Image.objects.count())
        print(slice_pos)

        # split queryset with the slice operation
        first_list = Image.objects.all()[:slice_pos]
        second_list = Image.objects.all()[slice_pos:]

        # merge the two sets with itertools/chain
        merged_queryset = list(chain(second_list, first_list))
        return merged_queryset

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
