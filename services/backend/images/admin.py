from django.contrib import admin

from images.models import Image, Thumbnail

admin.site.register(Image)
admin.site.register(Thumbnail)
