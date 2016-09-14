from django.views import generic
from gallery.models import Publisher


class ThankYouView(generic.DetailView):
    model = Publisher
    template_name = 'gallery/thankyou.html'


class PublishErrorView(generic.DetailView):
    model = Publisher
    template_name = 'gallery/publisherror.html'
