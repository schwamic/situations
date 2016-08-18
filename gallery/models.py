from django.db import models
from django.utils import timezone
import uuid


class Publisher(models.Model):
    alias = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    invited_by = models.ForeignKey('self', on_delete=models.CASCADE)
    date_of_birth = models.DateTimeField('date of birth')
    zip_code = models.IntegerField('zip code')
    is_active = models.BooleanField(default=True)
    active_time = models.DurationField()

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
        (7, 'Computer/Mathematical '),
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


class Image(models.Model):
    url = models.URLField(max_length=200)
    title = models.CharField(max_length=50)
    author = models.CharField(max_length=50)
    year = models.DateTimeField('year published')
    location = models.CharField(max_length=50)


class Post(models.Model):
    image = models.ForeignKey(Image, on_delete=models.CASCADE)
    publisher = models.ForeignKey(Publisher, on_delete=models.CASCADE)
    pub_date = models.DateTimeField('date published')
    description = models.CharField(max_length=500)
    reason = models.CharField(max_length=500)
