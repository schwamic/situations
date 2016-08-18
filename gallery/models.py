from django.db import models
import uuid

class Publisher(models.Model):
    pass

class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    image = models.ForeignKey(Image, on_delete=models.CASCADE)
    publisher = models.ForeignKey(Publisher, on_delete=models.CASCADE)
    pub_date = models.DateTimeField('date published')
    description = models.CharField(max_length=500)
    reason = models.CharField(max_length=500)

class Image(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    url = models.URLField(max_length=200)
    title = models.CharField(max_length=50)
    author = models.CharField(max_length=50)
    year = models.DateTimeField('year published')
    location = models.CharField(max_length=50)
