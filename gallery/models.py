from django.db import models


class Publisher(models.Model):
    invited_by = models.ForeignKey('self', on_delete=models.CASCADE)
    GENDER_MALE = 0
    GENDER_FEMALE = 1
    GENDER_CHOICES = [(GENDER_MALE, 'Male'), (GENDER_FEMALE, 'Female')]
    gender = models.IntegerField(choices=GENDER_CHOICES)

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
    occupation = models.ImageField(choices=OCCUPATION_CHOICES)

    date_of_birth = models.DateTimeField('date published')
    zip_code = models.IntegerField('zip code')
    is_active = models.BooleanField(default=True)
    active_time = models.DurationField()


class Post(models.Model):
    pass


class Image(models.Model):
    pass