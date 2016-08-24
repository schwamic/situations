from django.db import models
from datetime import datetime
from gallery import choices
import uuid


class Publisher(models.Model):
    verbose_id = models.UUIDField(default=uuid.uuid4)
    email = models.CharField('e-mail', max_length=50)
    invited_by = models.ForeignKey('self', blank=True, null=True, on_delete=models.CASCADE)
    date_of_birth = models.DateTimeField('date of birth', blank=True, null=True)
    zip_code = models.IntegerField('zip code', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    active_time = models.DurationField('time spent to publish', blank=True, null=True)
    gender = models.IntegerField(choices=choices.GENDER_CHOICES, default=choices.GENDER_MALE)
    occupation = models.IntegerField(choices=choices.OCCUPATION_CHOICES, default=0)

    def __str__(self):
        return self.email


class Image(models.Model):
    filename = models.CharField(max_length=200)
    title = models.CharField(max_length=50, default='Some Title')
    author = models.CharField(max_length=50, default='Some Author')
    date_photo_taken = models.DateTimeField('year photo taken', default=datetime.now())
    location = models.CharField(max_length=50, default='Some City')

    def __str__(self):
        return self.filename


class Post(models.Model):
    image = models.ForeignKey(Image, on_delete=models.CASCADE)
    publisher = models.ForeignKey(Publisher, on_delete=models.CASCADE)
    publishing_date = models.DateTimeField(default=datetime.now())
    description = models.CharField(max_length=200, default='Some description')
    reason = models.CharField(max_length=200, default='Some Reason')

    def __str__(self):
        return u'%s posted by %s' % (self.image, self.publisher)