import datetime

GENDER_MALE = 0
GENDER_FEMALE = 1
GENDER_CHOICES = [
    (GENDER_MALE, 'Male'),
    (GENDER_FEMALE, 'Female')
]

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


MIN_AGE = 10
START_YEAR = 1900
now = datetime.datetime.now()
END_YEAR = now.year - MIN_AGE

YEAR_BORN = []

for x in range(END_YEAR - START_YEAR):
    tup1 = (x, END_YEAR - x)
    YEAR_BORN.append(tup1)
