from django.contrib.gis.geoip2 import GeoIP2
from django.core.mail import EmailMessage
from django.shortcuts import get_object_or_404
from django.http import Http404, HttpResponse
from django.views import generic
from django.http import HttpResponseRedirect
from django.urls import reverse
from situations import settings
from gallery import choices
from itertools import chain
from .models import Publisher, Image, Post
from django.utils import timezone
import urllib
import json
from django.core import serializers

class ImagesView(generic.ListView):
    model = Image
    template_name = 'gallery/images.html'
    paginate_by = 36

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

        return uuid

    @staticmethod
    def get_slice_position(uuid, max_value):
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
        context['my_publisher_email'] = self.publisher.email
        context['my_publisher_verbose_id'] = self.publisher.verbose_id
        context['gender_choices'] = choices.GENDER_CHOICES
        context['occupation_choices'] = choices.OCCUPATION_CHOICES
        context['year_choices'] = choices.YEAR_BORN
        # pagination

        paginator = context.get('paginator')
        num_pages = paginator.num_pages
        current_page = context.get('page_obj')
        page_no = current_page.number

        if num_pages <= 8 or page_no <= 4:  # case 1 and 2
            pages = [x for x in range(1, min(num_pages + 1, 9))]
        elif page_no > num_pages - 6:  # case 4
            pages = [x for x in range(num_pages - 7, num_pages + 1)]
        else:  # case 3
            pages = [x for x in range(page_no - 3, page_no + 4)]

        context.update({'pages': pages})
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
                # ('location', '%s, %s, %s' % (post.publisher.city, post.publisher.region, post.publisher.country)),
                ('location', post.publisher.city),
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
    paginate_by = 18
    ordering = '-pk'

    def get_context_data(self, **kwargs):
        context = super(PostsView, self).get_context_data(**kwargs)

        if self.request.GET.get('id') is not None:
            context['lightbox_id'] = self.request.GET.get('id')
        else:
            context['lightbox_id'] = '-1'

        # pagination
        paginator = context.get('paginator')
        num_pages = paginator.num_pages
        current_page = context.get('page_obj')
        page_no = current_page.number

        if num_pages <= 8 or page_no <= 4:  # case 1 and 2
            pages = [x for x in range(1, min(num_pages + 1, 9))]
        elif page_no > num_pages - 6:  # case 4
            pages = [x for x in range(num_pages - 7, num_pages + 1)]
        else:  # case 3
            pages = [x for x in range(page_no - 3, page_no + 4)]

        context.update({'pages': pages})
        return context


class ThankYouView(generic.DetailView):
    model = Publisher
    template_name = 'gallery/thankyou.html'


class PublishError(generic.DetailView):
    model = Publisher
    template_name = 'gallery/publisherror.html'


def publish(request, publisher_id):
    success = False

    # get current publisher object
    publisher = get_object_or_404(Publisher, pk=publisher_id)
    if publisher.is_active is False:
        return HttpResponseRedirect(reverse('gallery:publisherror', args=(publisher_id,)))

    # add publisher attributes
    publisher.gender = int(request.POST['gender'])
    publisher.occupation = int(request.POST['occupation'])
    publisher.year_of_birth = int(request.POST['year_of_birth'])
    # print('year_of_birth: '+str(publisher.year_of_birth))

    publisher.active_time = timezone.now() - publisher.session_start
    publisher.is_active = False

    print(request.POST['latitude'])
    # add location info to publisher
    if request.POST['latitude'] != 'no_entry':
        # get additional geo data using google geo code api
        publisher.latitude = float(request.POST['latitude'])
        publisher.longitude = float(request.POST['longitude'])

        google_reverse_geo_code_url = \
            'https://maps.googleapis.com/maps/api/geocode/json?latlng=%s,%s&key=%s' % (
                publisher.latitude, publisher.longitude, settings.GOOGLE_API_KEY
            )
        google_api_response = urllib.urlopen(google_reverse_geo_code_url).read().decode(encoding='UTF-8')
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
        print('USER IP: ' + user_ip)

        if settings.DEV_MODE is 0:
            location = g.city('128.101.101.101')  # dummy ip for local testing, localhost wont work
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

    # invite new publisher
    try:
        email_1 = request.POST['email_1']
        email_2 = request.POST['email_2']
        invite_new_publisher(publisher, email_1)
        if email_2 != email_1:
            invite_new_publisher(publisher, email_2)
        success = True
    except:
        success = False

    # push to db
    if success is True:
        new_post.save()
        publisher.save()
    else:
        return HttpResponseRedirect(reverse('gallery:publisherror', args=(publisher_id,)))

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

    # send mail
    subject = 'Invitation to SITUATIONS from ' + parent.email

    '''
    file = open(MEDIA_ROOT + '/email/mail.txt', 'r')
    content = file.read()
    file.close()
    '''

    content = '<p><b>(Un)filtered Scenarios. An Experiment in Distributed Selection</b></p>'

    content += '<p>By receiving this mail, Fotomuseum Winterthur and Der Greif cordially invite you<br> ' \
              'to participate in a collectively curated online exhibition and a collaborative experiment on image<br> ' \
              'selection (read more here: <a href="https://www.dergreif-online.de/submit/call/29" style="color: black;">dergreif-online.de/submit/call/29</a>).</p>'

    content += '<p><b>Participating is simple:</b></p>'

    content += '<p><b>1. Select your favourite image and write a brief explanation of why you chose that<br>' \
               'specific picture.</b><br>'\
               'Access the database of images on the project-website using this link:<br>' \
               '<a href="'+settings.DOMAIN + 'images/?id=' + str(new_publisher.verbose_id) + '" style="color: black;">'+settings.DOMAIN + 'images/?id=' + str(new_publisher.verbose_id) +'</a></p>'

    content += '<p><b>2. Forward this email to two further participants of your choice.</b><br>' \
               'This project relies on user participation and we ask you to involve <b>two additional people</b><br>' \
               ' who will likely be happy to join the initiative and be part of this experiment.</p>'

    content += '<p>There are no restrictions to who is invited other than that they must be 18 years old (images<br>' \
               ' may contain explicit content). Should you receive this email more than once by different<br>' \
               'participants, we ask you to follow the invitation repeatedly.</p>'

    content += '<p>---------------------</p>'

    content += '<p>Please consult the project website <a href="http://situations.dergreif-online.de" style="color: black;">situations.dergreif-online.de</a> from 17.09 to<br>' \
               ' 27.11.2016 and follow the development of the online exhibition and experiment.</p>'

    content += '<p><b>In case you have any questions, we prepared a simple manual. Please download it<br>' \
               'here: <a href="http://situations.dergreif-online.de/media/pdf/manual.pdf" style="color: black;">situations.dergreif-online.de/manual</a></b><br>' \
               "If the manual doesn't answer all your questions, do not hesitate to get in touch with<br>" \
               '<a href="mailto:situations@dergreif-online.de" style="color: black;">situations@dergreif-online.de</a></p>'

    content += '<p>Many thanks for your participation, without which this project could not work!</p>'

    content += '<p>---------------------</p>'

    content += '<p>Please note that your participation will be anonymized and only depersonalized data will be<br>' \
               'made accessible and displayed in the form of maps and charts on the project website<br>' \
               '<a href="http://situations.dergreif-online.de" style="color: black;">situations.dergreif-online.de</a> and at Fotomuseum Winterthur from 17.09 to 27.11.2016<br>' \
               'as part of the exhibition SITUATIONS/Filter (<a href="http://situations.fotomuseum.ch" style="color: black;">situations.fotomuseum.ch</a>). </p><br><br>'

    msg = EmailMessage(
        subject,
        content,
        settings.DEFAULT_FROM_EMAIL,
        [new_publisher.email],
    )
    msg.content_subtype = "html"
    msg.send(fail_silently=False)

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

        response_data['publisher_id'] = post.publisher.name +'-'+ str(post.publisher.id)
        response_data['post_publishing_date'] = '%s.%s.%s' % (post.publishing_date.day, post.publishing_date.month, post.publishing_date.year)
        response_data['publisher_gender'] = choices.GENDER_CHOICES[int(post.publisher.gender)][1]
        response_data['publisher_occupation'] = choices.OCCUPATION_CHOICES[int(post.publisher.occupation)][1]
        response_data['publisher_age'] = int(timezone.now().year) - int(choices.YEAR_BORN[post.publisher.year_of_birth][1])
        response_data['publisher_location'] = str(post.publisher.city)+', '+str(post.publisher.country)
        response_data['publisher_active_time'] = str(post.publisher.active_time)
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

class AudioView(generic.ListView):
    model = Post
    template_name = 'gallery/audio.html'

class DataVisualisationView(generic.ListView):
    model = Publisher
    template_name = 'gallery/datavisualisation.html'


def d3_data(request):
    if request.method == 'GET':
        d3_data = serializers.serialize('json', Publisher.objects.all().filter(is_active=False)) # ,fields('name', 'next attr')
        return HttpResponse(json.dumps(d3_data), content_type="application/json")
    else:
        return HttpResponse(json.dumps({"nothing to see": "this isn't happening"}), content_type="application/json")

def d3_gender(request):
    if request.method == 'GET':

        gender = []
        for i, val in choices.GENDER_CHOICES:
            gender.append({"value": val, "publications": Publisher.objects.all().filter(occupation=i, is_active=False).count()})

        return HttpResponse(json.dumps(gender), content_type="application/json")
    else:
        return HttpResponse(json.dumps({"nothing to see": "this isn't happening"}), content_type="application/json")

def d3_occupation(request):
    if request.method == 'GET':
        occupation = []
        for i, val in choices.OCCUPATION_CHOICES:
            occupation.append({"name": val, "value": Publisher.objects.all().filter(occupation=i, is_active=False).count()})
        return HttpResponse(json.dumps(occupation), content_type="application/json")
    else:
        return HttpResponse(json.dumps({"nothing to see": "this isn't happening"}), content_type="application/json")

def d3_age(request):
    if request.method == 'GET':

        '''
        z.B. publications: 50 , age: 18
        <18
        19-15
        26-35
        36-50
        >51
        '''

        age = [
            {"publications": 100, "age": "<18"},
            {"publications": 500, "age": "19-15"},
            {"publications": 230, "age": "26-36"},
            {"publications": 800, "age": "36-50"},
            {"publications": 500, "age": ">51"}
        ]

        return HttpResponse(json.dumps(age), content_type="application/json")
    else:
        return HttpResponse(json.dumps({"nothing to see": "this isn't happening"}), content_type="application/json")

def d3_time_of_activity(request):
    if request.method == 'GET':
        publisher = get_object_or_404(Publisher, pk=1)
        publisher2 = get_object_or_404(Publisher, pk=2)
        publisher3 = get_object_or_404(Publisher, pk=3)
        publisher4 = get_object_or_404(Publisher, pk=4)
        publisher5 = get_object_or_404(Publisher, pk=5)
        post = get_object_or_404(Post, pk=1)

        print('%s-%s-%s' % (post.publishing_date.day, post.publishing_date.month, post.publishing_date.year))

        activity = [
            {"close": str(publisher.active_time), "open": 25, "date": "1-Mar-12"},
            {"close": str(publisher2.active_time), "open": 25, "date": "2-Mar-12"},
            {"close": str(publisher3.active_time), "open": 25, "date": "3-Mar-12"},
            {"close": str(publisher4.active_time), "open": 25, "date": "4-Mar-12"},
            {"close": str(publisher.active_time), "open": 25, "date": "5-Mar-12"},
            {"close": str(publisher2.active_time), "open": 25, "date": "6-Mar-12"},
            {"close": str(publisher3.active_time), "open": 25, "date": "7-Mar-12"},
            {"close": str(publisher4.active_time), "open": 25, "date": "8-Mar-12"},
            {"close": str(publisher.active_time), "open": 25, "date": "10-Mar-12"},
            {"close": str(publisher2.active_time), "open": 25, "date": "14-Mar-12"},
            {"close": str(publisher3.active_time), "open": 25, "date": "15-Mar-12"},
            {"close": str(publisher4.active_time), "open": 25, "date": "19-Mar-12"},
            {"close": str(publisher5.active_time), "open": 25, "date": "26-Mar-12"}
        ]

        return HttpResponse(json.dumps(activity), content_type="application/json")
    else:
        return HttpResponse(json.dumps({"nothing to see": "this isn't happening"}), content_type="application/json")


def d3_posts_per_day(request):
    if request.method == 'GET':
        # Participants (Posts)
        posts = [
            {"close": 3, "open": 25, "date": "1-Mar-12"},
            {"close": 4, "open": 25, "date": "2-Mar-12"},
            {"close": 5, "open": 25, "date": "3-Mar-12"},
            {"close": 7, "open": 25, "date": "4-Mar-12"},
            {"close": 31, "open": 25, "date": "5-Mar-12"},
            {"close": 33, "open": 25, "date": "6-Mar-12"},
            {"close": 34, "open": 25, "date": "7-Mar-12"},
            {"close": 50, "open": 25, "date": "8-Mar-12"},
            {"close": 77, "open": 25, "date": "9-Mar-12"},
            {"close": 91, "open": 25, "date": "10-Mar-12"},
            {"close": 113, "open": 25, "date": "11-Mar-12"},
            {"close": 114, "open": 25, "date": "12-Mar-12"},
            {"close": 150, "open": 25, "date": "13-Mar-12"},
            {"close": 177, "open": 25, "date": "14-Mar-12"},
            {"close": 231, "open": 25, "date": "15-Mar-12"},
            {"close": 243, "open": 25, "date": "16-Mar-12"},
            {"close": 246, "open": 25, "date": "17-Mar-12"},
            {"close": 250, "open": 25, "date": "18-Mar-12"},
            {"close": 277, "open": 25, "date": "19-Mar-12"},
            {"close": 281, "open": 25, "date": "20-Mar-12"},
        ]

        return HttpResponse(json.dumps(posts), content_type="application/json")
    else:
        return HttpResponse(json.dumps({"nothing to see": "this isn't happening"}), content_type="application/json")

# note:
# a[start:end] # items start through end-1
# a[start:]    # items start through the rest of the array
# a[:end]      # items from the beginning through end-1
# a[:]         # a copy of the whole array

# add session
# #self.request.session['current_publisher_id'] = uuid
# get session
# #publisher_id=request.session['current_publisher']
# print(publisher.id)

###########################################################
#
#   google dev acc: greif.situations
#               pw: DasIstSicher123
#
#   google api key: AIzaSyBs4ZYShxicQyYy_lZ5cOJlcFUqHHw1V9M
#
###########################################################