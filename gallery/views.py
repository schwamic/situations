from django.contrib.gis.geoip2 import GeoIP2
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django.http import Http404, HttpResponse
from django.views import generic
from django.http import HttpResponseRedirect
from django.urls import reverse
from situations import settings
from gallery import choices
from itertools import chain
from .models import Publisher, Image, Post
from django.core import serializers
from django.utils import timezone
import json
import random
import urllib.request


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

        self.publisher.session_start = timezone.now()
        self.publisher.save()
        print('called')

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
    model = Post
    template_name = 'gallery/map.html'

    @staticmethod
    def get_markers():
        markers = []

        for post in Post.objects.all():
            marker = [
                ('post_pk', post.pk),
                ('date', '%s.%s.%s' % (post.publishing_date.day, post.publishing_date.month, post.publishing_date.year)),
                ('publisher_pk', post.publisher.pk),
                ('gender', choices.GENDER_CHOICES[post.publisher.gender][1]),
                ('location', '%s, %s, %s' % (post.publisher.city, post.publisher.region, post.publisher.country)),
                ('publisher_lat', post.publisher.latitude),
                ('publisher_lng', post.publisher.longitude)
            ]

            if post.publisher.invited_by is not None:
                inv_by_lat = ('inv_by_lat', post.publisher.invited_by.latitude)
                inv_by_lng = ('inv_by_lng', post.publisher.invited_by.longitude)

                marker.append(inv_by_lat)
                marker.append(inv_by_lng)
            markers.append(marker)


        return markers

    def get_context_data(self, **kwargs):
        context = super(MapView, self).get_context_data(**kwargs)

        # dumps to json for js
        context['markers'] = json.dumps(self.get_markers())
        context['colors'] = json.dumps(settings.COLORS)
        context['mode'] = settings.MAP_MODE
        context['limit'] = settings.MAP_LIMIT

        return context


class PostsView(generic.ListView):
    model = Post
    template_name = 'gallery/posts.html'
    paginate_by = 15
    ordering = '-pk'


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
    publisher.active_time = timezone.now() - publisher.session_start
    publisher.is_active = False

    # add location info to publisher
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
        # FALLBACK: geo locating via geoIP2
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

    # invite new publisher
    invite_new_publisher(publisher, request.POST['email_1'])
    if request.POST['email_2'] is not '':
        invite_new_publisher(publisher, request.POST['email_2'])
    if request.POST['email_3'] is not '':
        invite_new_publisher(publisher, request.POST['email_3'])

    return HttpResponseRedirect(reverse('gallery:thankyou', args=(publisher_id,)))


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def invite_new_publisher(parent, mail_address):
    new_publisher = Publisher(
        email=mail_address,
        invited_by=parent
    )
    new_publisher.save()

    # sent mail
    subject = 'Invitation to SITUATIONS from ' + parent.email
    content = '[project description]\n'
    content += 'To participate, simply follow this link:\n'
    content += settings.DOMAIN + 'images/?id=' + str(new_publisher.verbose_id) + '\n\n'
    content += 'Please note: there is no need to log in or to create an account.\n'
    content += 'However, once the link has been used to publish, it will expire.\n\n'
    content += 'Thanks and have fun browsing!\n'
    content += '- SITUATIONS'
    send_mail(
        subject,
        content,
        parent.email,
        [new_publisher.email],
        fail_silently=False,
    )
    print('usr created, mail sent - subject: ' + subject)
    print('content : \n' + content)


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