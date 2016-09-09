from django.conf.urls import url
from django.views.generic import TemplateView
from . import views

app_name = 'gallery'
urlpatterns = [
    # root
    url(r'^$', views.PostsView.as_view(), name='root'),
    url(r'^detail_post/$', views.detail_post, name='detail_root'),

    # posts
    url(r'^posts/$', views.PostsView.as_view(), name='posts'),
    url(r'^posts/detail_post/$', views.detail_post, name='post_detail'),
    url(r'^posts/(?P<id>[0-9]+)/detail_post/$', views.detail_post, name='post_detail'),

    # map
    url(r'^map/$', views.MapView.as_view(), name='map'),
    url(r'^map/detail_post/$', views.detail_post, name='map_detail'),

    # images
    url(r'^images/$', views.ImagesView.as_view(), name='images'),
    url(r'^images/detail_image/$', views.detail_image, name='image_detail'),
    url(r'^images/(?P<publisher_id>[0-9]+)/publish/$', views.publish, name='publish'),
    url(r'^images/(?P<pk>[0-9]+)/thankyou/$', views.ThankYouView.as_view(), name='thankyou'),
    url(r'^images/(?P<pk>[0-9]+)/error/$', views.PublishError.as_view(), name='publisherror'),

    # static
    url(r'^about/$', TemplateView.as_view(template_name='gallery/about.html'), name="about"),
    url(r'^impressum/$', TemplateView.as_view(template_name='gallery/imprint.html'), name="impressum"),

    #data visualisation
    url(r'^datavisualisation/$', views.DataVisualisationView.as_view(), name='datavisualisation'),
    url(r'^datavisualisation/d3data/$', views.d3_data, name='d3_data'),
]

# uuid: (?P<something>[^/]+)
# number: (?P<something>[0-9]+)
