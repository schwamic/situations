from django.views import generic
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.core.serializers import serialize
from gallery.models import Publisher, Post
from gallery.choices import GENDER_CHOICES, OCCUPATION_CHOICES
import json


class DataVisualisationView(generic.ListView):
    model = Publisher
    template_name = 'gallery/datavisualisation.html'


def d3_data(request):
    if request.method == 'GET':
        d3_data = serialize('json', Publisher.objects.all().filter(is_active=False)) # ,fields('name', 'next attr')
        return HttpResponse(json.dumps(d3_data), content_type="application/json")
    else:
        return HttpResponse(json.dumps({"nothing to see": "this isn't happening"}), content_type="application/json")


def d3_gender(request):
    if request.method == 'GET':

        gender = []
        for i, val in GENDER_CHOICES:
            gender.append({"value": val, "publications": Publisher.objects.all().filter(occupation=i, is_active=False).count()})

        return HttpResponse(json.dumps(gender), content_type="application/json")
    else:
        return HttpResponse(json.dumps({"nothing to see": "this isn't happening"}), content_type="application/json")


def d3_occupation(request):
    if request.method == 'GET':
        occupation = []
        for i, val in OCCUPATION_CHOICES:
            occupation.append({"name": val, "value": Publisher.objects.all().filter(occupation=i, is_active=False).count()})
        return HttpResponse(json.dumps(occupation), content_type="application/json")
    else:
        return HttpResponse(json.dumps({"nothing to see": "this isn't happening"}), content_type="application/json")


def d3_age(request):
    if request.method == 'GET':

        '''
        z.B. publications: 50 , age: 18
        <18
        19-15
        26-35
        36-50
        >51
        '''

        age = [
            {"publications": 100, "age": "<18"},
            {"publications": 500, "age": "19-15"},
            {"publications": 230, "age": "26-36"},
            {"publications": 800, "age": "36-50"},
            {"publications": 500, "age": ">51"}
        ]

        return HttpResponse(json.dumps(age), content_type="application/json")
    else:
        return HttpResponse(json.dumps({"nothing to see": "this isn't happening"}), content_type="application/json")


def d3_time_of_activity(request):
    if request.method == 'GET':
        publisher = get_object_or_404(Publisher, pk=1)
        publisher2 = get_object_or_404(Publisher, pk=2)
        publisher3 = get_object_or_404(Publisher, pk=3)
        publisher4 = get_object_or_404(Publisher, pk=4)
        publisher5 = get_object_or_404(Publisher, pk=5)
        post = get_object_or_404(Post, pk=1)

        print('%s-%s-%s' % (post.publishing_date.day, post.publishing_date.month, post.publishing_date.year))

        activity = [
            {"close": str(publisher.active_time), "open": 25, "date": "1-Mar-12"},
            {"close": str(publisher2.active_time), "open": 25, "date": "2-Mar-12"},
            {"close": str(publisher3.active_time), "open": 25, "date": "3-Mar-12"},
            {"close": str(publisher4.active_time), "open": 25, "date": "4-Mar-12"},
            {"close": str(publisher.active_time), "open": 25, "date": "5-Mar-12"},
            {"close": str(publisher2.active_time), "open": 25, "date": "6-Mar-12"},
            {"close": str(publisher3.active_time), "open": 25, "date": "7-Mar-12"},
            {"close": str(publisher4.active_time), "open": 25, "date": "8-Mar-12"},
            {"close": str(publisher.active_time), "open": 25, "date": "10-Mar-12"},
            {"close": str(publisher2.active_time), "open": 25, "date": "14-Mar-12"},
            {"close": str(publisher3.active_time), "open": 25, "date": "15-Mar-12"},
            {"close": str(publisher4.active_time), "open": 25, "date": "19-Mar-12"},
            {"close": str(publisher5.active_time), "open": 25, "date": "26-Mar-12"}
        ]

        return HttpResponse(json.dumps(activity), content_type="application/json")
    else:
        return HttpResponse(json.dumps({"nothing to see": "this isn't happening"}), content_type="application/json")


def d3_posts_per_day(request):
    if request.method == 'GET':
        # Participants (Posts)
        posts = [
            {"close": 3, "open": 25, "date": "1-Mar-12"},
            {"close": 4, "open": 25, "date": "2-Mar-12"},
            {"close": 5, "open": 25, "date": "3-Mar-12"},
            {"close": 7, "open": 25, "date": "4-Mar-12"},
            {"close": 31, "open": 25, "date": "5-Mar-12"},
            {"close": 33, "open": 25, "date": "6-Mar-12"},
            {"close": 34, "open": 25, "date": "7-Mar-12"},
            {"close": 50, "open": 25, "date": "8-Mar-12"},
            {"close": 77, "open": 25, "date": "9-Mar-12"},
            {"close": 91, "open": 25, "date": "10-Mar-12"},
            {"close": 113, "open": 25, "date": "11-Mar-12"},
            {"close": 114, "open": 25, "date": "12-Mar-12"},
            {"close": 150, "open": 25, "date": "13-Mar-12"},
            {"close": 177, "open": 25, "date": "14-Mar-12"},
            {"close": 231, "open": 25, "date": "15-Mar-12"},
            {"close": 243, "open": 25, "date": "16-Mar-12"},
            {"close": 246, "open": 25, "date": "17-Mar-12"},
            {"close": 250, "open": 25, "date": "18-Mar-12"},
            {"close": 277, "open": 25, "date": "19-Mar-12"},
            {"close": 281, "open": 25, "date": "20-Mar-12"},
        ]

        return HttpResponse(json.dumps(posts), content_type="application/json")
    else:
        return HttpResponse(json.dumps({"nothing to see": "this isn't happening"}), content_type="application/json")