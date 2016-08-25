from django.contrib.gis.geoip2 import GeoIP2
from django.shortcuts import get_object_or_404
from django.http import Http404
from django.views import generic
from django.http import HttpResponseRedirect
from django.urls import reverse
from gallery import choices
#from django_ajax.decorators import ajax
from itertools import chain
from .models import Publisher, Image, Post

"""
use this url to access images (for now):
http://127.0.0.1:8000/images/?id=940e6d98-9f30-42a8-8c9a-c37b4e514c62
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
        context['my_publisher_id'] = self.publisher.id
        context['gender_choices'] = choices.GENDER_CHOICES
        context['occupation_choices'] = choices.OCCUPATION_CHOICES

        print(context)
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

    #get current publisher object
    publisher = get_object_or_404(Publisher, pk=publisher_id)
    #add all attr
    publisher.gender = int(request.POST['gender'])
    publisher.occupation = int(request.POST['occupation'])
    #publisher.year_of_birth = int(request.POST['year_of_birth'])

    #post
    description = request.POST['describtion']
    reason = request.POST['reason']
    image_id = request.POST.get('image')
    image = get_object_or_404(Image, pk=image_id)
    new_post = Post(image=image, publisher=publisher, description=description, reason=reason)

    # geo locating
    """
    user_ip = get_client_ip(request)
    location = GeoIP2.city(request, user_ip)
    publisher.city = location.city
    publisher.country = location.country_name
    publisher.region = location.region
    publisher.longitude = location.longitude
    publisher.latitude = location.latitude
    """
    #push to db
    new_post.save()
    publisher.save()

    return HttpResponseRedirect(reverse('gallery:thankyou', args=(publisher_id,)))


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


# note:
# a[start:end] # items start through end-1
# a[start:]    # items start through the rest of the array
# a[:end]      # items from the beginning through end-1
# a[:]         # a copy of the whole array

#add session
# #self.request.session['current_publisher_id'] = uuid
#get session
# #publisher_id=request.session['current_publisher']
#print(publisher.id)