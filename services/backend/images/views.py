import os

from django.conf import settings
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie
from rest_framework import viewsets, serializers
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from config.settings import CACHE_TTL
from helpers.create_thumbnail import create_thumbnail
from images.models import Image, Thumbnail
from images.serializers import ImageSerializer, ImageSerializerWithoutOriginalLink, ThumbnailGeneratorSerializer, \
    ThumbnailSerializer


class ImageViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Image.objects.filter(author=user)

    def get_serializer_class(self):
        user = self.request.user
        if user.tier.link_flag:
            return ImageSerializer
        else:
            return ImageSerializerWithoutOriginalLink

    @method_decorator(cache_page(CACHE_TTL))
    @method_decorator(vary_on_cookie)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


class ThumbnailViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def create(self, request):
        result = ThumbnailGeneratorSerializer(data=request.data, context={'user': request.user})
        if result.is_valid():
            heights = result.data.get('heights')
            image = Image.objects.get(author=request.user, pk=result.data.get('image_id'))
            heights_in_db = [thumbnail.height for thumbnail in Thumbnail.objects.filter(image=image)]

            thumbnail_urls = []
            for height in heights:
                if height not in heights_in_db:
                    thumbnail_name = create_thumbnail(image, height)
                    thumbnail_url = os.path.join('resized_images', thumbnail_name)
                    Thumbnail.objects.create(image=image, url=thumbnail_url, height=height)
                    thumbnail_urls.append(thumbnail_url)
                else:
                    thumbnail_urls.append(Thumbnail.objects.get(image_id=image.pk, height=height).url)

            thumbnail_urls = [f'{request.build_absolute_uri(settings.MEDIA_URL)}{url}' for url in thumbnail_urls]

            return Response({'links': thumbnail_urls})

        return Response(result.errors)

    @method_decorator(cache_page(CACHE_TTL))
    @method_decorator(vary_on_cookie)
    def retrieve(self, request, pk=None):
        image = Image.objects.filter(pk=pk, author=request.user)
        if not image:
            raise serializers.ValidationError('Image with given id does not exist.')

        queryset = Thumbnail.objects.filter(image__author=request.user, image_id=pk)
        serializer = ThumbnailSerializer(queryset, many=True, context={'request': request})

        return Response(serializer.data)
