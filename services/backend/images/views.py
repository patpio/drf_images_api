from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from images.models import Image
from images.serializers import ImageSerializer, ImageSerializerWithoutOriginalLink


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
