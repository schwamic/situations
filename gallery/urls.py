from django.conf.urls import url
from django.views.generic import TemplateView
from gallery.views import *

app_name = 'gallery'
urlpatterns = [
    # root
    url(r'^$', PostsView.as_view(), name='root'),
    url(r'^detail_post/$', detail_post, name='detail_root'),

    # posts
    url(r'^posts/$', PostsView.as_view(), name='posts'),
    url(r'^posts/detail_post/$', detail_post, name='post_detail'),
    url(r'^posts/(?P<id>[0-9]+)/detail_post/$', detail_post, name='post_detail'),

    # map
    url(r'^map/$', MapView.as_view(), name='map'),
    url(r'^map/detail_post/$', detail_post, name='map_detail'),

    # images
    url(r'^images/$', ImagesView.as_view(), name='images'),
    url(r'^images/detail_image/$', detail_image, name='image_detail'),
    url(r'^images/(?P<publisher_id>[0-9]+)/publish/$', publish, name='publish'),
    url(r'^images/(?P<pk>[0-9]+)/thankyou/$', ThankYouView.as_view(), name='thankyou'),
    url(r'^images/(?P<pk>[0-9]+)/error/$', PublishError.as_view(), name='publisherror'),

    # static
    url(r'^about/$', TemplateView.as_view(template_name='gallery/about.html'), name="about"),
    url(r'^imprint/$', TemplateView.as_view(template_name='gallery/imprint.html'), name="impressum"),

    #data visualisation
    url(r'^datavisualisation/$', DataVisualisationView.as_view(), name='datavisualisation'),
    url(r'^datavisualisation/d3_data/$', d3_data, name='d3_data'),
    url(r'^datavisualisation/d3_gender/$', d3_gender, name='d3_gender'),
    url(r'^datavisualisation/d3_occupation/$', d3_occupation, name='d3_occupation'),
    url(r'^datavisualisation/d3_age/$', d3_age, name='d3_age'),
]

# uuid: (?P<something>[^/]+)
# number: (?P<something>[0-9]+)
