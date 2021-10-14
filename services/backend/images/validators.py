import os
import magic
from django.conf import settings
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.core.exceptions import ValidationError


def validate_file_type(upload):
    tmp_path = 'tmp/%s' % upload.name[2:]
    default_storage.save(tmp_path, ContentFile(upload.file.read()))
    full_tmp_path = os.path.join(settings.MEDIA_ROOT, tmp_path)

    file_type = magic.from_file(full_tmp_path, mime=True)
    default_storage.delete(tmp_path)

    image_types = [f'image/{img}' for img in settings.IMAGE_TYPES]
    if file_type not in image_types:
        raise ValidationError(f'File type not supported. Use: {", ".join(settings.IMAGE_TYPES)}')
