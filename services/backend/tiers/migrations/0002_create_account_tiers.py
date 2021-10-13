from django.db import migrations


def generate_thumbnail_sizes(apps, schema_editor):
    Size = apps.get_model('tiers', 'Size')
    Size.objects.bulk_create(
        [
            Size(height=200),
            Size(height=400),
        ]
    )


def generate_account_tiers(apps, schema_editor):
    Tier = apps.get_model('tiers', 'Tier')
    Size = apps.get_model('tiers', 'Size')
    Tier.objects.bulk_create(
        [
            Tier(name='Basic'),
            Tier(name='Premium', link_flag=True),
            Tier(name='Enterprise', link_flag=True, expired_link_flag=True),
        ]
    )

    Tier.objects.get(name='Basic').size.add(Size.objects.get(height=200))
    Tier.objects.get(name='Premium').size.add(Size.objects.get(height=200), Size.objects.get(height=400))
    Tier.objects.get(name='Enterprise').size.add(Size.objects.get(height=200), Size.objects.get(height=400))


class Migration(migrations.Migration):
    dependencies = [
        ('tiers', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(generate_thumbnail_sizes),
        migrations.RunPython(generate_account_tiers)
    ]
