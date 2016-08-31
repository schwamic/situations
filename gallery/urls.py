from django.conf.urls import url
from django.views.generic import TemplateView
from . import views

app_name = 'gallery'
urlpatterns = [
    url(r'^$', views.PostsView.as_view(), name='posts'),
    url(r'^images/$', views.ImagesView.as_view(), name='images'),
    url(r'^posts/$', views.PostsView.as_view(), name='posts'),
    url(r'^map/$', views.MapView.as_view(), name='map'),
    url(r'^images/(?P<publisher_id>[0-9]+)/publish/$', views.publish, name='publish'),
    url(r'^images/(?P<pk>[[0-9]+)/thankyou/$', views.ThankYouView.as_view(), name='thankyou'),
    url(r'^images/detail_image/$', views.detail_image, name='detail_image'),
    url(r'^posts/detail_image/$', views.detail_image, name='detail_image'),
    url(r'^about/$', TemplateView.as_view(template_name='gallery/about.html'), name="about"),
    url(r'^impressum/$', TemplateView.as_view(template_name='gallery/impressum.html'), name="impressum"),
]
# note
# uuid: (?P<something>[^/]+)
# number: (?P<something>[0-9]+)