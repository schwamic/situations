from django.views import generic
from gallery.models import Post
from situations.settings import SHUFFLE, COLORS
import json


class AudioView(generic.ListView):
    model = Post
    template_name = 'gallery/audio.html'

    def get_context_data(self, **kwargs):
        context = super(AudioView, self).get_context_data(**kwargs)
        context['shuffle'] = SHUFFLE
        context['colors'] = json.dumps(COLORS)

        return context
