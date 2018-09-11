from django.db import models
from membership.models import Member

class Reward(models.Model):
    member = models.OneToOneField(Member, on_delete=models.SET_NULL, null=True)
    current_point = models.IntegerField(blank=True, default=0)
    lifetime_point = models.IntegerField(blank=True, default=0)