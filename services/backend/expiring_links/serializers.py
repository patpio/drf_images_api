from rest_framework import serializers

from images.models import Image


class ExpiringLinkGeneratorSerializer(serializers.Serializer):
    image_id = serializers.IntegerField(min_value=1)
    expiration_time = serializers.IntegerField()

    def validate(self, data):
        if not self.context['user'].tier.expired_link_flag:
            raise serializers.ValidationError('Your tier have no access for expiring links.')

        return data

    def validate_image_id(self, value):
        user = self.context['user']
        image = Image.objects.filter(pk=value, author=user)

        if not image:
            raise serializers.ValidationError('Image with given id does not exist.')

        return value

    def validate_expiration_time(self, value):
        if not 300 <= value <= 30000:
            raise serializers.ValidationError('Expiration time must be between 300 and 30000 seconds.')

        return value
