from django.views import generic
from gallery.models import Post
from gallery.choices import GENDER_CHOICES
from situations import settings
import json


class MapView(generic.ListView):
    model = Post
    template_name = 'gallery/map.html'

    @staticmethod
    def get_markers():
        # note for future projects:
        # get_markers creates a list, but should create a dictionary for jason dumps
        # even better way for creating a js interface in django is a custom api

        markers = []

        for post in Post.objects.all():
            marker = [
                ('post_pk', post.pk),
                ('date', '%s.%s.%s' % (post.publishing_date.day, post.publishing_date.month, post.publishing_date.year)),
                ('publisher_pk', post.publisher.pk),
                ('gender', GENDER_CHOICES[post.publisher.gender][1]),
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
