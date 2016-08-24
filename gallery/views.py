from django.shortcuts import get_object_or_404
from django.http import Http404
from django.views import generic
from itertools import chain
from .models import Publisher, Image, Post
from django.http import HttpResponseRedirect
from django.urls import reverse

"""
use this url to access images (for now):
http://127.0.0.1:8000/images/?id=a576a3f6-411a-4ac0-83b3-e174103cdf3a

its a working uuid in the current db
"""

class ImagesView(generic.ListView):
    model = Image
    template_name = 'gallery/images.html'
    paginate_by = 25

    def get_uuid(self):
        """
        collects request parm and checks correctness.
        returns a uuid if an associated user can be found.
        :return:
        """
        uuid = self.request.GET.get('id')

        self.publisher = get_object_or_404(Publisher, alias=uuid)


        if not self.publisher.is_active:
            raise Http404("Link already used or expired.")

        return uuid

    def get_slice_position(self, uuid, max_value):
        """
        generates a user specific value 0 <= x < max_value using
        :return:
        """
        uuid_generated_number = 1
        for count, letter in enumerate(uuid[:8]):  # first 8 numbers should be sufficient
            if count % 2 is 0:
                uuid_generated_number *= ord(letter)
            else:
                uuid_generated_number += ord(letter)
        return uuid_generated_number % max_value

    def get_queryset(self):
        slice_pos = self.get_slice_position(self.get_uuid(), Image.objects.count())

        # split queryset using the slice operation
        first_list = Image.objects.all()[:slice_pos]
        second_list = Image.objects.all()[slice_pos:]

        # merge the two sets using itertools/chain
        merged_queryset = list(chain(second_list, first_list))
        return merged_queryset

    def get_context_data(self, **kwargs):
        print(self.publisher.alias)
        context = {"publisher_id", self.publisher}
        return context


class MapView(generic.ListView):
    model = Post
    template_name = 'gallery/map.html'

class PostsView(generic.ListView):
    model = Post
    template_name = 'gallery/posts.html'
    paginate_by = 25


class ThankYouView(generic.DetailView):
    model = Publisher
    template_name = 'gallery/thankyou.html'

def publish(request):
    print("publisher start")

    return HttpResponseRedirect(reverse('gallery:thankyou', args=("")))

    #get session
   # publisher_id=request.session['current_publisher']
    #print(publisher.id)

    #publisher = get_object_or_404(Publisher, alias=id)
    #gender = publisher.GENDER_CHOICES(int(request.POST['gender']))
    #print(gender)


# note:
# a[start:end] # items start through end-1
# a[start:]    # items start through the rest of the array
# a[:end]      # items from the beginning through end-1
# a[:]         # a copy of the whole array

#add session
# #self.request.session['current_publisher_id'] = uuid
