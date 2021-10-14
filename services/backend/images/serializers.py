from rest_framework import serializers

from images.models import Image, Thumbnail


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = '__all__'
        read_only_fields = ['name']


class ImageSerializerWithoutOriginalLink(ImageSerializer):
    class Meta(ImageSerializer.Meta):
        extra_kwargs = {'url': {'write_only': True}}


class ThumbnailGeneratorSerializer(serializers.Serializer):
    image_id = serializers.IntegerField(min_value=1)
    heights = serializers.ListField(child=serializers.IntegerField(min_value=1), allow_empty=False)

    def validate_image_id(self, value):
        user = self.context['user']
        image = Image.objects.filter(pk=value, author=user)

        if not image:
            raise serializers.ValidationError('Image with given id does not exist.')

        return value

    def validate_heights(self, value):
        user = self.context['user']
        available_heights = [size.height for size in user.tier.size.all()]

        for height in value:
            if height not in available_heights:
                raise serializers.ValidationError(
                    f'Chosen height ({height} px) is not available in your tier ({user.tier}).')

        return value


class ThumbnailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Thumbnail
        fields = '__all__'
