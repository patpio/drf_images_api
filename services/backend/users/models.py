from django.contrib.auth.models import AbstractUser
from django.db import models

from tiers.models import Tier


class CustomUser(AbstractUser):
    tier = models.ForeignKey(Tier, on_delete=models.SET_NULL, related_name='tiers', null=True)
