import os
from datetime import timedelta
from uuid import uuid4

from django.conf import settings
from django.http import FileResponse
from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from expiring_links.models import ExpiringLink
from expiring_links.serializers import ExpiringLinkGeneratorSerializer
from images.models import Image


class ExpiringLinkView(viewsets.ViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def create(self, request):
        result = ExpiringLinkGeneratorSerializer(data=request.data, context={'user': request.user})
        if result.is_valid():
            token = uuid4()
            image_id = result.data.get('image_id')
            duration = result.data.get('expiration_time')
            image = Image.objects.get(pk=image_id)
            image_url = image.url
            image_extension = image.name.rsplit('.')[-1]

            ExpiringLink.objects.create(url=image_url, token=token, duration=duration)

            url = f'{request.build_absolute_uri()}{token}.{image_extension}'

            return Response({'link': url})

        return Response(result.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, token):
        token = token.split('.')[0]
        obj = get_object_or_404(ExpiringLink, token=token)
        expiration_date = obj.created_at + timedelta(seconds=obj.duration)

        if expiration_date <= timezone.now():
            return Response(f'Link is no more available. Expiration date: {expiration_date}.',
                            status=status.HTTP_400_BAD_REQUEST)

        return FileResponse(open(os.path.join(settings.MEDIA_URL[1:], obj.url), 'rb'))
