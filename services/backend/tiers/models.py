from django.db import models


class Tier(models.Model):
    name = models.CharField(max_length=30)
    link_flag = models.BooleanField(default=False, verbose_name='Link for original image',
                                    help_text='Can user see link for original image?')
    expired_link_flag = models.BooleanField(default=False, verbose_name='Expiring links',
                                            help_text='Can user create expiring links?')
    size = models.ManyToManyField('Size', related_name='tier')

    def __str__(self):
        return f'{self.name}'


class Size(models.Model):
    height = models.PositiveIntegerField(default=200, verbose_name='Height in px')

    def __str__(self):
        return f'{self.height} px'
