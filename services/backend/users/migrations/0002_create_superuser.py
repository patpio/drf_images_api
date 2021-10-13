import os

from django.db import migrations


def generate_superuser(apps, schema_editor):
    from django.contrib.auth import get_user_model
    User = get_user_model()

    DJANGO_SU_NAME = os.environ.get('DJANGO_SU_NAME')
    DJANGO_SU_EMAIL = os.environ.get('DJANGO_SU_EMAIL')
    DJANGO_SU_PASSWORD = os.environ.get('DJANGO_SU_PASSWORD')

    User.objects.create_superuser(
        username=DJANGO_SU_NAME,
        email=DJANGO_SU_EMAIL,
        password=DJANGO_SU_PASSWORD,
        tier_id=3
    )


class Migration(migrations.Migration):
    dependencies = [
        ('users', '0001_initial'),
        ('tiers', '0002_create_account_tiers')
    ]

    operations = [
        migrations.RunPython(generate_superuser)
    ]
