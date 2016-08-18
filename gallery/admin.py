from django.contrib import admin

# Register your models here.
from .models import Publisher
from .models import Image
from .models import Post


admin.site.register(Publisher)
admin.site.register(Image)
admin.site.register(Post)