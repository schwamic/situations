from django.db import models
from datetime import datetime
import uuid


class Publisher(models.Model):
    verbose_id = models.UUIDField(default=uuid.uuid4)
    email = models.CharField('e-mail', max_length=50)
    invited_by = models.ForeignKey('self', blank=True, null=True, on_delete=models.CASCADE)
    date_of_birth = models.DateTimeField('date of birth')
    zip_code = models.IntegerField('zip code')
    is_active = models.BooleanField(default=True)
    active_time = models.DurationField('time spent to publish', blank=True, null=True)

    GENDER_MALE = 0
    GENDER_FEMALE = 1
    GENDER_CHOICES = [(GENDER_MALE, 'Male'), (GENDER_FEMALE, 'Female')]
    gender = models.IntegerField(choices=GENDER_CHOICES, default=GENDER_MALE)

    OCCUPATION_CHOICES = [
        (0, 'Management'),
        (1, 'Office/Administrative Support'),
        (2, 'Business and Financial Operations '),
        (3, 'Architecture/Engineering'),
        (4, 'Art and Design'),
        (5, 'Entertainer/Performer'),
        (6, 'Media and Communications'),
        (7, 'Computer/Mathematical'),
        (8, 'Farming/Fishing/Forestry Worker'),
        (9, 'Building and Grounds Cleaning and Maintenance'),
        (10, 'Life Science'),
        (11, 'Physical Science'),
        (12, 'Military and Protective Service'),
        (13, 'Healthcare Practitioner or Technician'),
        (14, 'Healthcare Support'),
        (15, 'Community and Social Service'),
        (16, 'Social Science'),
        (17, 'Legal Occupations'),
        (18, 'Education/Training/Library'),
        (19, 'Transportation'),
        (20, 'Personal Care and Service'),
        (21, 'Construction/Installation/Repair'),
        (22, 'Food Preparation/Serving'),
        (23, 'Sales'),
        (24, 'Production/Manufacturing'),
    ]
    occupation = models.IntegerField(choices=OCCUPATION_CHOICES, default=0)

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