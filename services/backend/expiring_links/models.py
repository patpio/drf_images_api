from django.db import models


class ExpiringLink(models.Model):
    url = models.URLField()
    token = models.UUIDField()
    created_at = models.DateTimeField(auto_now_add=True)
    duration = models.IntegerField()

    def __str__(self):
        return f'{self.url}'
