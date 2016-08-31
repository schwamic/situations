from django.contrib.gis.geoip2 import GeoIP2
from django.shortcuts import get_object_or_404, render
from django.http import Http404, HttpResponse
from django.views import generic
from django.http import HttpResponseRedirect
from django.urls import reverse
from situations import settings
from gallery import choices
from itertools import chain
from .models import Publisher, Image, Post
from django.core.serializers.json import DjangoJSONEncoder
from django.core import serializers
import json
import random
import urllib.request

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
        context['year_choices'] = choices.YEAR_BORN

        print(context)
        return context


class MapView(generic.ListView):
    template_name = 'gallery/map.html'

    def get_queryset(self):
        return Publisher.objects.filter(is_active=False).exclude(latitude__isnull=True, longitude__isnull=True)

    def get_context_data(self, **kwargs):
        context = super(MapView, self).get_context_data(**kwargs)
        context['publisher_data'] = serializers.serialize("json", self.get_queryset())

        return context


class PostsView(generic.ListView):
    model = Post
    template_name = 'gallery/posts.html'
    paginate_by = 15


class ThankYouView(generic.DetailView):
    model = Publisher
    template_name = 'gallery/thankyou.html'


def publish(request, publisher_id):
    # get current publisher object
    publisher = get_object_or_404(Publisher, pk=publisher_id)

    # add publisher attributes
    publisher.gender = int(request.POST['gender'])
    publisher.occupation = int(request.POST['occupation'])
    publisher.year_of_birth = int(request.POST['year_of_birth'])
    if request.POST['latitude'] != 'no_entry':
        # get additional geo data using google geo code api
        publisher.latitude = float(request.POST['latitude'])
        publisher.longitude = float(request.POST['longitude'])

        google_reverse_geo_code_url =\
            'https://maps.googleapis.com/maps/api/geocode/json?latlng=%s,%s&key=%s' % (
                publisher.latitude, publisher.longitude, settings.GOOGLE_API_KEY
            )
        google_api_response = urllib.request.urlopen(google_reverse_geo_code_url).read().decode(encoding='UTF-8')
        geo_data = json.loads(google_api_response)

        for result in geo_data['results']:
            for address_component in result['address_components']:
                if address_component['types'] == ['locality', 'political']:
                    publisher.city = address_component['long_name']
                    break
                if address_component['types'] == ['administrative_area_level_1', 'political']:
                    publisher.region = address_component['short_name']
                    break
                if address_component['types'] == ['country', 'political']:
                    publisher.country = address_component['long_name']
                    break

    else:
        # geo locating via geoIP2 --- FALLBACK
        user_ip = get_client_ip(request)
        g = GeoIP2()

        if settings.DEBUG:
            location = g.city('128.101.101.101')  # dummy ip for testing, localhost wont work
            print('user dummy ip: %s (debug true -> ip using: 128.101.101.101' % user_ip)
        else:
            location = g.city(user_ip)

        publisher.city = location['city']
        publisher.region = location['region']
        publisher.country = location['country_name']
        publisher.latitude = location['latitude']
        publisher.longitude = location['longitude']

    if settings.DEBUG:
        print('city: %s' % publisher.city)
        print('region: %s' % publisher.region)
        print('country: %s' % publisher.country)
        print('latitude: %s' % publisher.latitude)
        print('longitude: %s' % publisher.longitude)

    # post
    description = request.POST['description']
    reason = request.POST['reason']
    image_id = request.POST.get('image')
    image = get_object_or_404(Image, pk=image_id)
    new_post = Post(image=image, publisher=publisher, description=description, reason=reason)

    # push to db
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


def detail_image(request):
    if request.method == 'POST':
        image_id = request.POST.get('image_id')
        image = get_object_or_404(Image, pk=image_id)
        print(image_id)

        response_data = {}
        response_data['image_title'] = image.title
        response_data['image_author'] = image.author
        response_data['image_filename'] = '/media/'+image.filename
        response_data['image_count'] = Image.objects.count()

        return HttpResponse(
            json.dumps(response_data),
            content_type="application/json"
        )
    else:
        return HttpResponse(
            json.dumps({"nothing to see": "this isn't happening"}),
            content_type="application/json"
        )

def detail_post(request):
    if request.method == 'POST':
        post_id = request.POST.get('post_id')
        post = get_object_or_404(Post, pk=post_id)
        print(post_id)

        response_data = {}

        response_data['publisher_id'] = str(random.randint(100000, 999999))+'-'+str(post.publisher.id)
        response_data['post_publishing_date'] = str(post.publishing_date.date())
        response_data['publisher_gender'] = choices.GENDER_CHOICES[int(post.publisher.gender)][1]
        response_data['publisher_occupation'] = choices.OCCUPATION_CHOICES[int(post.publisher.occupation)][1]
        #response_data['publisher_age'] = choices.YEAR_BORN[post.publisher.year_of_birth][1]
        response_data['publisher_age'] = str(post.publisher.year_of_birth)
        response_data['publisher_location'] = str(post.publisher.city)+', '+str(post.publisher.country)
        #response_data['publisher_active_time'] = post.publisher.active_time
        response_data['post_description'] = post.description
        response_data['post_reason'] = post.reason

        response_data['image_author'] = post.image.author
        response_data['image_title'] = post.image.title
        response_data['image_filename'] = '/media/'+post.image.filename
        response_data['post_count'] = Post.objects.count()


        return HttpResponse(
            json.dumps(response_data),
            content_type="application/json"
        )
    else:
        return HttpResponse(
            json.dumps({"nothing to see": "this isn't happening"}),
            content_type="application/json"
        )

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

###########################################################
#
#   google dev acc: greif.situations
#               pw: DasIstSicher123
#
#   google api key: AIzaSyBs4ZYShxicQyYy_lZ5cOJlcFUqHHw1V9M
#
###########################################################