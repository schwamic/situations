from django.shortcuts import get_object_or_404
from django.http import Http404
from django.template import Context
from django.views import generic
from itertools import chain
from .models import Publisher, Image, Post
from django.http import HttpResponseRedirect
from django.urls import reverse

"""
use this url to access images (for now):
http://127.0.0.1:8000/images/?id=50719aab-a33b-441e-979d-a8a2533984a5
its a working uuid in the current db
"""


class ImagesView(generic.ListView):
    model = Image
    template_name = 'gallery/images.html'
    paginate_by = 30

    def get_uuid(self):
        """
        collects request parm and checks correctness.
        returns a uuid if an associated user can be found.
        :return:
        """
        uuid = self.request.GET.get('id')

        self.publisher = get_object_or_404(Publisher, verbose_id=uuid)


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
        context = super(ImagesView, self).get_context_data(**kwargs)
        context['my_publisher'] = self.publisher
        print(context);
        return context


class MapView(generic.ListView):
    model = Post
    template_name = 'gallery/map.html'


class PostsView(generic.ListView):
    model = Post
    template_name = 'gallery/posts.html'
    paginate_by = 15


class ThankYouView(generic.DetailView):
    model = Publisher
    template_name = 'gallery/thankyou.html'


def publish(request, publisher_id):

    print("publisher start")
    publisher = get_object_or_404(Publisher, pk=publisher_id)
    print(publisher.email)

    #get session
    #publisher_id=request.session['current_publisher']
    #print(publisher.id)

    #publisher = get_object_or_404(Publisher, alias=id)
    #gender = publisher.GENDER_CHOICES(int(request.POST['gender']))
    #print(gender)
    return HttpResponseRedirect(reverse('gallery:thankyou', args=(publisher_id,)))

# note:
# a[start:end] # items start through end-1
# a[start:]    # items start through the rest of the array
# a[:end]      # items from the beginning through end-1
# a[:]         # a copy of the whole array

#add session
# #self.request.session['current_publisher_id'] = uuid
