from django.views import generic
from django.http import HttpResponse
from django.core import serializers
from gallery.models import Publisher, Post
from gallery import choices
import json
from django.utils import timezone
from datetime import timedelta
from datetime import datetime

class DataVisualisationView(generic.ListView):
    model = Publisher
    template_name = 'gallery/datavisualisation.html'

def d3_data(request):
    if request.method == 'GET':
        d3_data = serializers.serialize('json', Publisher.objects.all().filter(is_active=False)) #,fields('name', 'next attr')
        return HttpResponse(json.dumps(d3_data), content_type="application/json")
    else:
        return HttpResponse(json.dumps({"nothing to see": "this isn't happening"}), content_type="application/json")

def d3_gender(request):
    if request.method == 'GET':

        gender = []
        for i, val in choices.GENDER_CHOICES:
            gender.append({"value": val, "publications": Publisher.objects.all().filter(gender=i, is_active=False).count()})

        return HttpResponse(json.dumps(gender), content_type="application/json")
    else:
        return HttpResponse(json.dumps({"nothing to see": "this isn't happening"}), content_type="application/json")

def d3_occupation(request):
    if request.method == 'GET':
        occupation = []
        for i, val in choices.OCCUPATION_CHOICES:
            occupation.append({"name": val, "value": Publisher.objects.all().filter(occupation=i, is_active=False).count()})
        return HttpResponse(json.dumps(occupation), content_type="application/json")
    else:
        return HttpResponse(json.dumps({"nothing to see": "this isn't happening"}), content_type="application/json")

def d3_age(request):
    if request.method == 'GET':

        group_one = 0
        group_two = 0
        group_three = 0
        group_four = 0
        group_five = 0

        for obj in Publisher.objects.all().filter(is_active=False):
            years = (int(timezone.now().year) - int(choices.YEAR_BORN[obj.year_of_birth][1]))
            if years <= 17:
                group_one += 1

            elif (years >= 18) and (years <= 25):
                group_two += 1

            elif (years >= 26) and (years <= 35):
                group_three += 1

            elif (years >= 36) and (years <= 50):
                group_four += 1

            elif years >= 51:
                group_five += group_five + 1

            else:
                return "no match found."

        age = [
            {"publications": group_one, "age": "<18"},
            {"publications": group_two, "age": "18-15"},
            {"publications": group_three, "age": "26-36"},
            {"publications": group_four, "age": "36-50"},
            {"publications": group_five, "age": ">50"}
        ]

        return HttpResponse(json.dumps(age), content_type="application/json")
    else:
        return HttpResponse(json.dumps({"nothing to see": "this isn't happening"}), content_type="application/json")

def d3_time_of_activity(request):
    if request.method == 'GET':

        def time_to_int(time):
            seconds = time.total_seconds()
            int_time = (int(seconds)/60/60)
            return int_time

        # fill width empty days and posts
        date1 = Post.objects.first().publishing_date.date()
        date2 = Post.objects.last().publishing_date.date()
        list_activity = []

        def date_range_filter(my_date):
            return (datetime.combine(my_date, datetime.min.time()), datetime.combine(my_date, datetime.max.time()))

        def daterange(d1, d2):
            return (d1 + timedelta(days=i) for i in range((d2 - d1).days + 1))

        for d in daterange(date1, date2):
            print('TEST +++++++'+str(Post.objects.all().filter(publishing_date__range=date_range_filter(d))))

            try:
                list_posts = Post.objects.all().filter(publishing_date__range=date_range_filter(d))
                if len(list_posts) > 0:
                    count = 0
                    for obj in list_posts:
                        count += time_to_int(obj.publisher.active_time)
                    list_activity.append({"close": count, "date": str(d)})
                else:
                    list_activity.append({"close": 0, "date": str(d)})
            except AttributeError as ae:
                print(ae)

        return HttpResponse(json.dumps(list_activity), content_type="application/json")
    else:
        return HttpResponse(json.dumps({"nothing to see": "this isn't happening"}), content_type="application/json")


def d3_posts_per_day(request):
    if request.method == 'GET':
        # Participants (Posts)

        # fill width empty days and posts

        date1 = Post.objects.first().publishing_date.date()
        date2 = Post.objects.last().publishing_date.date()
        list_participants = []
        count = 0

        def date_range_filter(my_date):
            return (datetime.combine(my_date, datetime.min.time()), datetime.combine(my_date, datetime.max.time()))

        def daterange(d1, d2):
            return (d1 + timedelta(days=i) for i in range((d2 - d1).days + 1))

        for d in daterange(date1, date2):
            print('TEST +++++++'+str(Post.objects.all().filter(publishing_date__range=date_range_filter(d))))

            try:
                list_posts = Post.objects.all().filter(publishing_date__range=date_range_filter(d))
                if len(list_posts) > 0:
                    for obj in list_posts:
                        count += 1
                    list_participants.append({"close": count, "date": str(d)})
                else:
                    list_participants.append({"close": count, "date": str(d)})
            except AttributeError as ae:
                print(ae)

        return HttpResponse(json.dumps(list_participants), content_type="application/json")
    else:
        return HttpResponse(json.dumps({"nothing to see": "this isn't happening"}), content_type="application/json")
