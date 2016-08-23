from django.contrib import admin

# Register your models here.
from .models import Publisher
from .models import Image
from .models import Post

class PublisherAdmin(admin.ModelAdmin):
    list_display = ('alias', 'name', 'occupation', 'email', 'is_active', 'invited_by')
    search_fields = ('alias', 'name', 'email',)
    list_filter = ('is_active', 'gender', 'occupation')

class ImageAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'filename')
    search_fields = ('title', 'author')

class PostAdmin(admin.ModelAdmin):
    list_display = ('image', 'publisher')
    search_fields = ('pub_date', 'image')

admin.site.register(Publisher, PublisherAdmin)
admin.site.register(Image, ImageAdmin)
admin.site.register(Post, PostAdmin)