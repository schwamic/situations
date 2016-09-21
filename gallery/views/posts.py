from django.views import generic
from django.utils import timezone
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from gallery.models import Post
from gallery.choices import GENDER_CHOICES, OCCUPATION_CHOICES, YEAR_BORN
import json


class PostsView(generic.ListView):
    model = Post
    template_name = 'gallery/posts.html'
    paginate_by = 18
    ordering = '-pk'

    def get_context_data(self, **kwargs):
        context = super(PostsView, self).get_context_data(**kwargs)

        if self.request.GET.get('id') is not None:
            context['lightbox_id'] = self.request.GET.get('id')
        else:
            context['lightbox_id'] = '-1'

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


def post_detail(request):
    if request.method == 'POST':
        post_id = request.POST.get('post_id')
        post = get_object_or_404(Post, pk=post_id)
        print(post_id)

        response_data = {}

        response_data['publisher_id'] = u'%s-%s' % (post.publisher.name, post.publisher.id)
        response_data['post_publishing_date'] = '%s.%s.%s' % (post.publishing_date.day, post.publishing_date.month,
                                                              post.publishing_date.year)
        response_data['publisher_gender'] = GENDER_CHOICES[int(post.publisher.gender)][1]
        response_data['publisher_occupation'] = OCCUPATION_CHOICES[int(post.publisher.occupation)][1]
        response_data['publisher_age'] = int(timezone.now().year) - int(YEAR_BORN[post.publisher.year_of_birth][1])
        response_data['publisher_location'] = u'%s, %s' % (post.publisher.city, post.publisher.country)
        response_data['publisher_active_time'] = str(post.publisher.active_time)
        response_data['post_description'] = post.description
        response_data['post_reason'] = post.reason

        response_data['image_author'] = post.image.author
        response_data['image_title'] = post.image.title
        response_data['image_filename'] = '/media/'+post.image.filename
        response_data['post_count'] = Post.objects.count()

        '''
        response_data['publisher_id'] = post.publisher.name + '-' + str(post.publisher.id)
        response_data['post_publishing_date'] = '%s.%s.%s' % (post.publishing_date.day, post.publishing_date.month,
                                                              post.publishing_date.year)
        response_data['publisher_gender'] = GENDER_CHOICES[int(post.publisher.gender)][1]
        response_data['publisher_occupation'] = OCCUPATION_CHOICES[int(post.publisher.occupation)][1]
        response_data['publisher_age'] = int(timezone.now().year) - int(YEAR_BORN[post.publisher.year_of_birth][1])
        response_data['publisher_location'] = str(post.publisher.city)+', '+str(post.publisher.country)
        response_data['publisher_active_time'] = str(post.publisher.active_time)
        response_data['post_description'] = post.description
        response_data['post_reason'] = post.reason

        response_data['image_author'] = post.image.author
        response_data['image_title'] = post.image.title
        response_data['image_filename'] = '/media/'+post.image.filename
        response_data['post_count'] = Post.objects.count()
        '''

        return HttpResponse(
            json.dumps(response_data),
            content_type="application/json"
        )
    else:
        return HttpResponse(
            json.dumps({"nothing to see": "this isn't happening"}),
            content_type="application/json"
        )
