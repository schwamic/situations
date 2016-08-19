from django.conf.urls import url

from . import views

app_name = 'gallery'
urlpatterns = [
    url(r'^$', views.PostsView.as_view(), name='posts'),
    url(r'^images/$', views.ImagesView.as_view(), name='images'),
]