from django.views import generic
from django.utils import timezone
from django.shortcuts import get_object_or_404
from django.http import Http404, HttpResponse
from gallery.models import Image, Publisher
from gallery.choices import GENDER_CHOICES, OCCUPATION_CHOICES, YEAR_BORN
from itertools import chain
import json


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
        context['gender_choices'] = GENDER_CHOICES
        context['occupation_choices'] = OCCUPATION_CHOICES
        context['year_choices'] = YEAR_BORN
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


def image_detail(request):
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
