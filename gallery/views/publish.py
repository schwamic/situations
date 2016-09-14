from django.contrib.gis.geoip2 import GeoIP2
from django.core.mail import EmailMessage
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.http import HttpResponseRedirect
from django.urls import reverse
from situations import settings
from gallery.models import Publisher, Image, Post
import urllib
import json

#########################################################
#
#   NOTE:   do not take this as an example in future for
#           future projects.
#
#   publish 'view' has some weird code in it.
#   lots of it is very likely to -NOT- be best practice.
#
#########################################################


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
    except Exception as e:
        print('++++++++++++++++++++++++++++++++ EMAIL EXEPTION')
        print(e)
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
               '<a href="'+settings.DOMAIN + 'images/?id=' + str(new_publisher.verbose_id) + '" style="color: black;">' + settings.DOMAIN + 'images/?id=' + str(new_publisher.verbose_id) +'</a></p>'

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
