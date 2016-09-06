from django.db import models
from gallery import choices
from django.utils import timezone
from datetime import timedelta
import uuid
import random


class Publisher(models.Model):
    # values generated on object creation
    verbose_id = models.UUIDField(default=uuid.uuid4)
    email = models.CharField('e-mail', max_length=50)
    invited_by = models.ForeignKey('self', blank=True, null=True, on_delete=models.CASCADE)
    name = models.CharField('name', max_length=50, default=str(random.randint(100000, 999999)))

    # values generated on runtime
    city = models.CharField(max_length=50, blank=True, null=True, default='some city')
    country = models.CharField(max_length=50, blank=True, null=True, default='some country')
    region = models.CharField(max_length=50, blank=True, null=True, default='some region')
    longitude = models.FloatField(blank=True, null=True)
    latitude = models.FloatField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    active_time = models.DurationField('time spent to publish', blank=True, null=True, default=timedelta(minutes=1))
    session_start = models.DateTimeField(blank=True, null=True)
    session_end = models.DateTimeField(blank=True, null=True)
    # user input, defaults needed?
    year_of_birth = models.IntegerField(choices=choices.YEAR_BORN, blank=True, null=True, default=0)
    gender = models.IntegerField(choices=choices.GENDER_CHOICES, default=choices.GENDER_MALE)
    occupation = models.IntegerField(choices=choices.OCCUPATION_CHOICES, default=0)

    def __str__(self):
        return self.email


class Image(models.Model):
    filename = models.CharField(max_length=200)
    title = models.CharField(max_length=50, default='Some Title')
    author = models.CharField(max_length=50, default='Some Author')
    date_photo_taken = models.DateTimeField('year photo taken', default=timezone.now)
    location = models.CharField(max_length=50, default='Some City')

    def __str__(self):
        return self.filename


class Post(models.Model):
    image = models.ForeignKey(Image, on_delete=models.CASCADE)
    publisher = models.ForeignKey(Publisher, on_delete=models.CASCADE)
    publishing_date = models.DateTimeField(default=timezone.now)
    description = models.CharField(max_length=200, default='Some description')
    reason = models.CharField(max_length=200, default='Some Reason')

    def __str__(self):
        return u'%s posted by %s' % (self.image, self.publisher)