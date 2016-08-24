from django.conf.urls import url
from . import views

app_name = 'gallery'
urlpatterns = [
    url(r'^$', views.PostsView.as_view(), name='posts'),
    url(r'^images/$', views.ImagesView.as_view(), name='images'),
    url(r'^posts/$', views.PostsView.as_view(), name='posts'),
    url(r'^map/$', views.MapView.as_view(), name='map'),
    url(r'^images/(?P<id>[^/]+)/publish/$', views.publish, name='publish'),
    url(r'^images/(?P<id>[^/]+)/$', views.ThankYouView.as_view(), name='thankyou'),
]

# note
# uuid: (?P<something>[^/]+)
# number: (?P<something>[0-9]+)